+++
title = "Три компаса"
date = "2022-01-11"
+++



# Три компаса

Ниже можно поэкспериментировать с тремя компасами из задачи с обложки январского номера "Квантика" за 2022 год.
Автор симуляции - Сергей Шашков.

Попробуйте перетащить компасы и увидите, как меняют положение стрелки.

Заряд иглы: 
<div id="needle_q" class="slider"></div>

Заряд полюса: 
<div id="pole_q" class="slider"></div>

Вязкость:
<div id="friction" class="slider"></div>

<div style="display:none;">
Максимальная сила: 
<div id="max_force" class="slider"></div>
</div>

<link href="style.css" rel="stylesheet">
<link href="nouislider.min.css" rel="stylesheet">
<script src="nouislider.min.js"></script>
<div id="Compass" style="width: 100%; max-width: 2000px;"></div>
<script src="main.js"  type="module"></script>
