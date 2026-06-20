"""
animations.py - JavaScript Animations & Interactive Effects
LaptopHealthPrediction | Portfolio Project

All animations are injected as <script> blocks via gr.HTML()
"""


# ─── Particle System (Hero Background) ───────────────────────────────────────

def get_particle_canvas_html() -> str:
    """
    Floating particles animation for hero background.
    Returns HTML with embedded canvas + JS.
    """
    return """
    <div id="particle-container" style="
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    ">
      <canvas id="particleCanvas"></canvas>
    </div>

    <script>
    (function() {
      const canvas = document.getElementById('particleCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');

      let width, height, particles = [];
      const PARTICLE_COUNT = 60;
      const COLORS = ['#7c3aed', '#a855f7', '#06b6d4', '#00f5a0', '#ffffff'];

      function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      }

      function randomBetween(a, b) { return a + Math.random() * (b - a); }

      function createParticle() {
        return {
          x: randomBetween(0, width),
          y: randomBetween(0, height),
          vx: randomBetween(-0.3, 0.3),
          vy: randomBetween(-0.5, -0.1),
          size: randomBetween(1, 3),
          opacity: randomBetween(0.1, 0.6),
          color: COLORS[Math.floor(Math.random() * COLORS.length)],
          life: 0,
          maxLife: randomBetween(150, 300),
          pulse: randomBetween(0, Math.PI * 2),
          pulseSpeed: randomBetween(0.02, 0.05),
        };
      }

      function initParticles() {
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
          particles.push(createParticle());
        }
      }

      function drawParticle(p) {
        p.pulse += p.pulseSpeed;
        const pulsedOpacity = p.opacity * (0.7 + 0.3 * Math.sin(p.pulse));
        const pulsedSize = p.size * (0.9 + 0.1 * Math.sin(p.pulse));

        ctx.save();
        ctx.globalAlpha = pulsedOpacity;
        ctx.fillStyle = p.color;
        ctx.shadowColor = p.color;
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.arc(p.x, p.y, pulsedSize, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      function drawConnections() {
        const maxDist = 120;
        for (let i = 0; i < particles.length; i++) {
          for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < maxDist) {
              const opacity = (1 - dist / maxDist) * 0.15;
              ctx.save();
              ctx.globalAlpha = opacity;
              ctx.strokeStyle = '#7c3aed';
              ctx.lineWidth = 0.5;
              ctx.beginPath();
              ctx.moveTo(particles[i].x, particles[i].y);
              ctx.lineTo(particles[j].x, particles[j].y);
              ctx.stroke();
              ctx.restore();
            }
          }
        }
      }

      function update() {
        ctx.clearRect(0, 0, width, height);
        drawConnections();

        particles.forEach((p, i) => {
          p.x += p.vx;
          p.y += p.vy;
          p.life++;

          // Fade in/out
          if (p.life < 30) p.opacity = (p.life / 30) * 0.6;
          if (p.life > p.maxLife - 30) p.opacity = ((p.maxLife - p.life) / 30) * 0.6;

          drawParticle(p);

          // Respawn
          if (p.life >= p.maxLife || p.y < -10 || p.x < -10 || p.x > width + 10) {
            particles[i] = createParticle();
          }
        });

        requestAnimationFrame(update);
      }

      resize();
      initParticles();
      update();
      window.addEventListener('resize', () => { resize(); initParticles(); });
    })();
    </script>
    """


# ─── Typing Animation ─────────────────────────────────────────────────────────

def get_typing_animation_html(
    element_id: str,
    texts: list,
    speed: int = 60,
    pause: int = 2000,
) -> str:
    """
    Typewriter animation cycling through multiple texts.
    
    Args:
        element_id: ID of the span to animate
        texts: List of strings to cycle through
        speed: Typing speed in ms per character
        pause: Pause between strings in ms
    """
    texts_json = str(texts).replace("'", '"')
    return f"""
    <script>
    (function() {{
      const el = document.getElementById('{element_id}');
      if (!el) return;

      const texts = {texts_json};
      let textIdx = 0, charIdx = 0, isDeleting = false;

      function type() {{
        const current = texts[textIdx];
        
        if (isDeleting) {{
          el.textContent = current.substring(0, charIdx - 1);
          charIdx--;
        }} else {{
          el.textContent = current.substring(0, charIdx + 1);
          charIdx++;
        }}

        // Blinking cursor
        el.style.borderRight = '2px solid #7c3aed';

        let delay = isDeleting ? {speed // 2} : {speed};

        if (!isDeleting && charIdx === current.length) {{
          delay = {pause};
          isDeleting = true;
        }} else if (isDeleting && charIdx === 0) {{
          isDeleting = false;
          textIdx = (textIdx + 1) % texts.length;
          delay = 300;
        }}

        setTimeout(type, delay);
      }}

      setTimeout(type, 500);
    }})();
    </script>
    """


# ─── Counter Animation ────────────────────────────────────────────────────────

def get_counter_animation_js(element_id: str, target: float, duration: int = 1500, suffix: str = "") -> str:
    """Animate a number counting up from 0 to target."""
    return f"""
    <script>
    (function() {{
      const el = document.getElementById('{element_id}');
      if (!el) return;
      const start = performance.now();
      const end = start + {duration};
      const target = {target};

      function easeOut(t) {{ return 1 - Math.pow(1 - t, 3); }}

      function step(now) {{
        const progress = Math.min((now - start) / (end - start), 1);
        const value = target * easeOut(progress);
        el.textContent = (Number.isInteger(target) ? Math.round(value) : value.toFixed(1)) + '{suffix}';
        if (progress < 1) requestAnimationFrame(step);
      }}

      requestAnimationFrame(step);
    }})();
    </script>
    """


# ─── Gradient Background Shift ────────────────────────────────────────────────

def get_gradient_shift_html() -> str:
    """Animated gradient background that slowly shifts colors."""
    return """
    <style>
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .animated-gradient-bg {
        background: linear-gradient(-45deg, #0a0a1a, #1a0a2e, #0a1a2e, #0a1a0e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    </style>
    """


# ─── Ripple Effect on Button Click ───────────────────────────────────────────

def get_ripple_effect_js(button_selector: str = ".predict-btn") -> str:
    """Add ripple click effect to a button."""
    return f"""
    <script>
    (function() {{
      function addRipple(e) {{
        const btn = e.currentTarget;
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position:absolute;
            border-radius:50%;
            background:rgba(255,255,255,0.25);
            transform:scale(0);
            animation:ripple-effect 0.6s linear;
            left:${{x - 50}}px;
            top:${{y - 50}}px;
            width:100px;
            height:100px;
            pointer-events:none;
        `;

        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.appendChild(ripple);
        setTimeout(() => ripple.remove(), 650);
      }}

      document.querySelectorAll('{button_selector}').forEach(btn => {{
        btn.addEventListener('click', addRipple);
      }});
    }})();

    <style>
    @keyframes ripple-effect {{
        to {{ transform:scale(4); opacity:0; }}
    }}
    </style>
    </script>
    """


# ─── Notification Toast System ────────────────────────────────────────────────

def get_toast_system_html() -> str:
    """Inject the global toast notification system."""
    return """
    <div id="toast-container" style="
        position:fixed;
        top:24px; right:24px;
        z-index:99999;
        display:flex;
        flex-direction:column;
        gap:10px;
        pointer-events:none;
    "></div>

    <script>
    window.showToast = function(message, type='success', duration=4000) {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const colors = {
            success: { bg:'rgba(0,245,160,0.1)', border:'rgba(0,245,160,0.4)', text:'#00f5a0', icon:'✅' },
            error: { bg:'rgba(255,107,107,0.1)', border:'rgba(255,107,107,0.4)', text:'#ff6b6b', icon:'❌' },
            warning: { bg:'rgba(249,212,35,0.1)', border:'rgba(249,212,35,0.4)', text:'#f9d423', icon:'⚠️' },
            info: { bg:'rgba(6,182,212,0.1)', border:'rgba(6,182,212,0.4)', text:'#06b6d4', icon:'ℹ️' },
            critical: { bg:'rgba(255,0,0,0.1)', border:'rgba(255,0,0,0.4)', text:'#ff5555', icon:'🚨' },
        };

        const c = colors[type] || colors.info;
        const toast = document.createElement('div');
        toast.style.cssText = `
            background: ${c.bg};
            border: 1px solid ${c.border};
            color: ${c.text};
            padding: 14px 20px;
            border-radius: 14px;
            font-size: 14px;
            font-weight: 600;
            font-family: Inter, sans-serif;
            backdrop-filter: blur(20px);
            max-width: 360px;
            pointer-events: auto;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            animation: slideInRight 0.4s ease;
            cursor: pointer;
        `;
        toast.innerHTML = `<span style="font-size:18px;">${c.icon}</span><span>${message}</span>`;
        toast.addEventListener('click', () => toast.remove());

        container.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'fadeOutRight 0.4s ease forwards';
            setTimeout(() => toast.remove(), 400);
        }, duration);
    };
    </script>

    <style>
    @keyframes slideInRight {
        from { opacity:0; transform:translateX(40px); }
        to { opacity:1; transform:translateX(0); }
    }
    @keyframes fadeOutRight {
        from { opacity:1; transform:translateX(0); }
        to { opacity:0; transform:translateX(40px); }
    }
    </style>
    """


# ─── Skeleton Loader ──────────────────────────────────────────────────────────

def get_skeleton_loader_html(lines: int = 5) -> str:
    """Build a skeleton loading placeholder."""
    bars = ""
    widths = [90, 75, 85, 60, 70]
    for i in range(lines):
        w = widths[i % len(widths)]
        bars += f"""
        <div style="
          background: linear-gradient(90deg,
            rgba(255,255,255,0.05) 25%,
            rgba(255,255,255,0.1) 50%,
            rgba(255,255,255,0.05) 75%
          );
          background-size: 200% 100%;
          animation: skeleton-loading 1.5s infinite;
          border-radius: 8px;
          height: 14px;
          width: {w}%;
          margin-bottom: 10px;
        "></div>"""

    return f"""
    {bars}
    <style>
    @keyframes skeleton-loading {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}
    </style>
    """


# ─── Prediction Loading Animation ────────────────────────────────────────────

def get_prediction_loading_html() -> str:
    """Show while model is running inference."""
    return """
    <div style="
      display:flex; flex-direction:column;
      align-items:center; justify-content:center;
      padding:50px 20px; gap:20px;
      animation: fadeIn 0.3s ease;
    ">

      <!-- Triple spinner -->
      <div style="position:relative; width:90px; height:90px;">
        <div style="
          position:absolute; inset:0;
          border:2px solid rgba(124,58,237,0.15);
          border-top-color:#7c3aed;
          border-radius:50%;
          animation:spin 0.9s linear infinite;
        "></div>
        <div style="
          position:absolute; inset:10px;
          border:2px solid rgba(6,182,212,0.15);
          border-top-color:#06b6d4;
          border-radius:50%;
          animation:spin 1.3s linear infinite reverse;
        "></div>
        <div style="
          position:absolute; inset:20px;
          border:2px solid rgba(0,245,160,0.15);
          border-top-color:#00f5a0;
          border-radius:50%;
          animation:spin 1.7s linear infinite;
        "></div>
        <div style="
          position:absolute; inset:30px;
          background:linear-gradient(135deg,#7c3aed,#06b6d4);
          border-radius:50%;
          animation:pulse-glow 1.5s ease-in-out infinite;
          display:flex; align-items:center; justify-content:center;
          font-size:18px;
        ">🤖</div>
      </div>

      <div style="text-align:center;">
        <p style="font-size:17px; font-weight:700; color:#fff; margin:0; font-family:'Space Grotesk',sans-serif;">
          AI Thinking...
        </p>
        <p style="font-size:12px; color:rgba(255,255,255,0.4); margin-top:6px;">
          Querying 100 Random Forest trees
        </p>
      </div>

      <!-- Animated dots -->
      <div style="display:flex; gap:6px;">
        <div style="width:8px;height:8px;background:#7c3aed;border-radius:50%;
                    animation:bounce-dot 1.2s ease infinite 0s;"></div>
        <div style="width:8px;height:8px;background:#a855f7;border-radius:50%;
                    animation:bounce-dot 1.2s ease infinite 0.2s;"></div>
        <div style="width:8px;height:8px;background:#06b6d4;border-radius:50%;
                    animation:bounce-dot 1.2s ease infinite 0.4s;"></div>
      </div>
    </div>

    <style>
      @keyframes spin { to { transform:rotate(360deg); } }
      @keyframes pulse-glow {
        0%,100% { box-shadow:0 0 15px rgba(124,58,237,0.4); transform:scale(0.95); }
        50% { box-shadow:0 0 30px rgba(124,58,237,0.7); transform:scale(1.05); }
      }
      @keyframes bounce-dot {
        0%,100% { transform:translateY(0); }
        50% { transform:translateY(-8px); }
      }
      @keyframes fadeIn { from{opacity:0;} to{opacity:1;} }
    </style>
    """


# ─── AI Thinking Status Texts ─────────────────────────────────────────────────

AI_THINKING_TEXTS = [
    "🌲 Traversing decision tree #1...",
    "🔍 Analyzing CPU utilization patterns...",
    "💾 Evaluating memory pressure...",
    "📊 Computing ensemble predictions...",
    "🤖 Aggregating 100 tree outputs...",
    "⚡ Calculating health score...",
    "🎯 Applying threshold analysis...",
    "✅ Generating recommendations...",
]


def get_typewriter_status_html(element_id: str = "ai-status") -> str:
    """Animated cycling status text during prediction."""
    texts_str = str(AI_THINKING_TEXTS).replace("'", '"')
    return f"""
    <div id="{element_id}" style="
      font-size:12px; font-family:'JetBrains Mono', monospace;
      color:rgba(124,58,237,0.8);
      text-align:center; min-height:20px;
    "></div>
    <script>
    (function() {{
      const el = document.getElementById('{element_id}');
      if (!el) return;
      const texts = {texts_str};
      let i = 0;
      function cycle() {{
        el.style.opacity = '0';
        setTimeout(() => {{
          el.textContent = texts[i % texts.length];
          el.style.opacity = '1';
          i++;
        }}, 200);
      }}
      cycle();
      const interval = setInterval(cycle, 1200);
      setTimeout(() => clearInterval(interval), texts.length * 1200 + 2000);
    }})();
    </script>
    <style>
    #{element_id} {{ transition: opacity 0.2s ease; }}
    </style>
    """


if __name__ == "__main__":
    print("✅ animations.py loaded!")
    print(f"Particle HTML length: {len(get_particle_canvas_html())} chars")
    print(f"Toast system HTML length: {len(get_toast_system_html())} chars")