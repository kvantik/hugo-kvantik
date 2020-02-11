var throws = [];
var sums = [];
var last_dice = [];
var prelast_dice = [];
const stop = 100;
function update_statistics(dice){
  sums.push(dice.sum[dice.sum.length-1]);
  last_dice.push(dice.dice[dice.dice.length-1]);
  prelast_dice.push(dice.dice[dice.dice.length-2]);
  throws.push(throws.length+1);
  return dice;
}

function throw_dice(max_sum = stop-1, dice_sides = 6){
  let i_array = [], dice_array = [], sum_array = [];
  let i = 0, sum = 0;
  while (sum<=max_sum) {
    i+=1;
    dice = Math.floor(Math.random() * dice_sides) + 1;
    sum += dice;
    i_array.push(i);
    dice_array.push(dice);
    sum_array.push(sum);
  }
  result = {i:i_array, dice:dice_array, sum:sum_array};
  update_statistics(result);
  return result;
}

function throw_series(n = 20){
  let dice;
  for (let i = 0; i < n; i++)
    dice = throw_dice();
  plot_single(dice);  
  //plot_all();  
  plot_stat();  
}