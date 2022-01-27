const WIDTH = 900;
const HEIGHT = 600;
const COMPASS_COLORS = ['#FF0000', '#00FF00', '#0000FF'];
// const COMPASS_COLORS = ['#FF0000', '#00FF00'];
// const COMPASS_COLORS = ['#FF0000'];
const COMPASS_DIAMETER = 150;
const NEEDLE_RADIUS = COMPASS_DIAMETER * 0.5 * 0.85;
const NORTH_NEEDLE_STYLE = {width: 10, "stroke-linecap": "round", color: "blue", opacity: 0.5};
const SOUTH_NEEDLE_STYLE = {width: 10, "stroke-linecap": "round", color: "red", opacity: 0.5};
const POLE_POS = [0, -10000];

const PARMS = {
  NEEDLE_Q: -2,
  POLE_Q: 3000,
  FRICTION: 0.01,
  MAX_FORCE: 0.05,
};


export function updateParms(newParm) {
  Object.assign(PARMS, newParm);
  console.log(PARMS)
}


// npm install @svgdotjs/svg.js
// Используем динамическую подгрузку, чтобы было легко вставлять симуляцию в тильду
function loadScript(src, integrity) {
  return new Promise(function (resolve, reject) {
    const script = document.createElement('script');
    script.src = src;
    if (integrity) {
      script.crossOrigin = 'anonymous';
      script.integrity = integrity;
    }
    script.onload = script.onreadystatechange = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

class FPSconsoleLogger {
  constructor(window = 10) {
    this.WINDOW = window;
    this.samples = Array(this.WINDOW).fill(0);
    this.samplePos = 0;
  }

  addDelta(dt) {
    this.samples[(this.samplePos++) % this.WINDOW] = dt;
    if (this.samplePos % this.WINDOW === 0) {
      console.log(this.FPS, 'fps');
    }
  }

  get FPS() {
    return ~~(1000 * this.WINDOW / this.samples.reduce((total, val) => total += val, 0));
  }
}

const loggerFPS = new FPSconsoleLogger();

const scene = {
  prevTime: null,
  animationFrame: null,
  paused: false,
  parentEl: null,
  compasses: null,
  isBeingDrugged: 0,
};


function compassDragStart(event) {
  scene.isBeingDrugged += 1;
  if (!scene.animationFrame) {
    resume();
  }
}

function compassDragMove(event) {
  const compass = event.detail.handler.el.rev;
  if (!compass) {
    console.error('Что-то не так с eventом, компас не найден');
  }
  const {cx, cy} = event.detail.box;
  Object.assign(compass, {cx, cy});
  compass.northLine.plot(cx, cy, ...needleEnd(cx, cy, compass.angle));
  compass.southLine.plot(cx, cy, ...needleEnd(cx, cy, compass.angle, -1));
}

function compassDragEnd(event) {
  scene.isBeingDrugged -= 1;
}

function needleEnd(cx, cy, angle, inv = 1) {
  return [cx + NEEDLE_RADIUS * Math.cos(angle) * inv, cy + NEEDLE_RADIUS * Math.sin(angle) * inv];
}

function initScene(draw) {
  draw.rect("100%", "100%").attr({fill: '#E9F8FE'});
  const compasses = COMPASS_COLORS.map((color, index) => {
    const cx = WIDTH / 6 + index * WIDTH / 3;
    const cy = HEIGHT / 2;
    const angle = -Math.PI / 4;
    return {
      id: index,
      cx,
      cy,
      circle: draw.circle(COMPASS_DIAMETER).fill(color).opacity(0.5).center(cx, cy),
      northLine: draw.line(cx, cy, ...needleEnd(cx, cy, angle)).stroke(NORTH_NEEDLE_STYLE),
      southLine: draw.line(cx, cy, ...needleEnd(cx, cy, angle, -1)).stroke(SOUTH_NEEDLE_STYLE),
      needleSpeed: 0,
      color: color,
      angle,
    };
  });
  for (const compass of compasses) {
    // Благодаря rev-ссылке мы найдём подробности об объекте и перерисуем ему стрелки
    compass.circle.rev = compass;
    compass.circle.draggable();
    compass.circle.on('dragstart.namespace', compassDragStart);
    compass.circle.on('dragmove.namespace', compassDragMove);
    compass.circle.on('dragend.namespace', compassDragEnd);
  }
  return {compasses};
}

function calcForce(x1, y1, x2, y2, Q1, Q2) {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const distSquared = dx * dx + dy * dy;
  const dist = Math.sqrt(distSquared);
  const sgn = Q1 * Q2 > 0 ? 1 : -1;
  const absValue = sgn * Math.min(Math.abs(Q1 * Q2 / distSquared), PARMS.MAX_FORCE/1000);
  // console.log({absValue});
  return [dx / dist * absValue, dy / dist * absValue];
}


function updateNeedlesSpeed(dt) {
  // Изменение скорости равно силе умножить на dt
  for (const compass1 of scene.compasses) {
    // Вычисляем координаты концов стрелок
    const [cnx1, cny1] = needleEnd(compass1.cx, compass1.cy, compass1.angle);
    const [csx1, csy1] = needleEnd(compass1.cx, compass1.cy, compass1.angle, -1);
    // Суммируем все силы. Сначала силы от полюса
    let [fx, fy] = calcForce(cnx1, cny1, ...POLE_POS, PARMS.NEEDLE_Q, PARMS.POLE_Q);
    let addF = calcForce(csx1, csy1, ...POLE_POS, -PARMS.NEEDLE_Q, PARMS.POLE_Q);
    fx += -addF[0]; // Минус, так как сила к южному полюсу
    fy += -addF[1];
    for (const compass2 of scene.compasses) {
      if (compass1 === compass2) continue;
      const [cnx2, cny2] = needleEnd(compass2.cx, compass2.cy, compass2.angle);
      const [csx2, csy2] = needleEnd(compass2.cx, compass2.cy, compass2.angle, -1);
      const fNN = calcForce(cnx1, cny1, cnx2, cny2, PARMS.NEEDLE_Q, PARMS.NEEDLE_Q);
      const fNS = calcForce(cnx1, cny1, csx2, csy2, PARMS.NEEDLE_Q, -PARMS.NEEDLE_Q);
      const fSN = calcForce(csx1, csy1, cnx2, cny2, -PARMS.NEEDLE_Q, PARMS.NEEDLE_Q);
      const fSS = calcForce(csx1, csy1, csx2, csy2, -PARMS.NEEDLE_Q, -PARMS.NEEDLE_Q);
      fx += fNN[0] + fNS[0] - fSN[0] - fSS[0];
      fy += fNN[1] + fNS[1] - fSN[1] - fSS[1];
    }
    // Вычисляем единичный вектор нормали к одному из концов, ориентированный «по часовой»
    let [nx, ny] = [cnx1 - compass1.cx, cny1 - compass1.cy];
    [nx, ny] = [ny, -nx];
    const ln = Math.sqrt(nx * nx + ny * ny);
    [nx, ny] = [nx / ln, ny / ln];
    // Все, [nx, ny] — вектор единичной нормали к северному концу компаса, а [fx, fy] — суммарный вектор силы
    // [fx, fy] проецируем на нормаль, получаем момент
    const momentum = nx * fx + ny * fy;
    compass1.needleSpeed += momentum * dt;
    // Теперь добавляем вязкое трение
    compass1.needleSpeed -= PARMS.FRICTION * compass1.needleSpeed * dt;
  }
}

function updateNeedlesAngles(dt) {
  for (const compass of scene.compasses) {
    compass.angle += compass.needleSpeed * dt;
  }
}

function replotNeedles() {
  for (const compass of scene.compasses) {
    compass.northLine.plot(compass.cx, compass.cy, ...needleEnd(compass.cx, compass.cy, compass.angle));
    compass.southLine.plot(compass.cx, compass.cy, ...needleEnd(compass.cx, compass.cy, compass.angle, -1));
  }
}


function animate(time) {
  const dt = time - scene.prevTime;
  scene.prevTime = time;
  // Не обсчитываем чаще, чем 120 раз за секунду (а ещё пропускаем «кадры», если dt вдруг отрицательный. Явно же косяк в учёте времени на старте анимации)
  if (dt < 1000 / 120) {
    scene.animationFrame = requestAnimationFrame(animate);
    return;
  }
  updateNeedlesSpeed(dt);
  updateNeedlesAngles(dt);
  replotNeedles();
  // loggerFPS.addDelta(dt); // Выводим в console.log текущий FPS
  // if (!scene.drag) {
  //   cancelAnimationFrame(scene.animationFrame);
  //   scene.animationFrame = undefined;
  // } else {
  scene.animationFrame = requestAnimationFrame(animate);
  // }
}

function pause(ev) {
  scene.paused = true;
  cancelAnimationFrame(scene.animationFrame);
  scene.animationFrame = undefined;
}

function resume(ev) {
  scene.paused = false;
  scene.prevTime = performance.now();
  scene.animationFrame = requestAnimationFrame(animate);
}

function handleVisibilityChange() {
  if (document.hidden) {
    pause();
  } else {
    resume();
  }
}

// Создание симуляции
function run(el) {
  const appendToDomElement = el instanceof HTMLElement ? el : document.getElementById(el);
  scene.parentEl = appendToDomElement;
  // Нужно передать либо dom-элемент, либо id. Если id, то начать с #
  const draw = SVG().addTo(appendToDomElement).size(WIDTH, HEIGHT);

  window.addEventListener('blur', pause);
  window.addEventListener('pagehide', pause);
  window.addEventListener('focus', resume);
  window.addEventListener('pageshow', resume);
  document.addEventListener('visibilitychange', handleVisibilityChange, false);

  Object.assign(scene, initScene(draw));
}

// Сначала загружаем svg.js, затем запускаем создание симуляции
export function addCompassSimulatorToEl(el) {
  // loadScript(
  //   'https://cdnjs.cloudflare.com/ajax/libs/svg.js/3.1.1/svg.min.js',
  //   'sha512-Aj0P6wguH3GVlCfbvTyMM90Zq886ePyMEYlZooRfx+3wcSYyUa6Uv4iAjoJ7yiWdKamqQzKp7yr/TkMQ8EEWbQ==',
  // ).then(() => run(el));
  loadScript('svg.min.js')
    .then(() => loadScript('svg.draggable.min.js'))
    .then(() => run(el));
}

export function removeCompassSimulator() {
  pause();
  dragStop();
  window.removeEventListener('blur', pause);
  window.removeEventListener('pagehide', pause);
  window.removeEventListener('focus', resume);
  window.removeEventListener('pageshow', resume);
  document.removeEventListener('visibilitychange', handleVisibilityChange, false);
  scene.parentEl.firstChild.remove();
}
