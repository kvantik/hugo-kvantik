import('./Compass.js').then((Compass) => {
  window.Compassjs = Compass;
  Compass.addCompassSimulatorToEl('Compass');
});

var slider_needle_q = document.getElementById('needle_q');
var slider_pole_q = document.getElementById('pole_q');
var slider_friction = document.getElementById('friction');
var slider_max_force = document.getElementById('max_force');

noUiSlider.create(slider_needle_q, {
  start: -1,
  step: 0.5,
  tooltips: true,
  range: {
    'min': -10,
    'max': 0,
  },
  pips: {
    mode: 'steps',
    stepped: true,
    density: 2,
  },
});


noUiSlider.create(slider_pole_q, {
  start: 3000,
  step: 500,
  tooltips: true,
  range: {
    'min': -10000,
    'max': 10000,
  },
  pips: {
    mode: 'steps',
    stepped: true,
    density: 4,
  },
});


noUiSlider.create(slider_friction, {
  start: 0.05,
  step: 0.005,
  tooltips: true,
  range: {
    'min': 0,
    'max': 0.1,
  },
  pips: {
    mode: 'steps',
    stepped: true,
    density: 4,
  },
});


noUiSlider.create(slider_max_force, {
  start: 0.05,
  step: 0.01,
  tooltips: true,
  range: {
    'min': 0,
    'max': 1,
  },
  pips: {
    mode: 'steps',
    stepped: true,
    density: 4,
  },
});


setTimeout(() => { 

 slider_needle_q.noUiSlider.on('update', function () {
  const NEEDLE_Q = slider_needle_q.noUiSlider.get();  
  window.Compassjs.updateParms({NEEDLE_Q});
 });


 slider_pole_q.noUiSlider.on('update', function () {
  const POLE_Q = slider_pole_q.noUiSlider.get();
  window.Compassjs.updateParms({POLE_Q});
 });


 slider_friction.noUiSlider.on('update', function () {
  const FRICTION = slider_friction.noUiSlider.get();
  window.Compassjs.updateParms({FRICTION});
 });


 slider_max_force.noUiSlider.on('update', function () {
  const MAX_FORCE = slider_max_force.noUiSlider.get();
  window.Compassjs.updateParms({MAX_FORCE});
 });

}, 400);
