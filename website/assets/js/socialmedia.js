$(function() {

  $('.hatena').socialbutton('hatena',  {
    button: 'vertical'
  });

  $('.twitter').socialbutton('twitter',  {
    button: 'vertical',
    text: document.title,
  });

  $('.facebook_like').socialbutton('facebook_like',  {
    button: 'box_count'
  });
  $('.hatena_mini').socialbutton('hatena');

  $('.twitter_mini').socialbutton('twitter',  {
    button: 'horizonal',
    text: document.title + ' - 多忙なあなたのタスク管理を全力で支援します',
  });

  $('.facebook_like_mini').socialbutton('facebook_like',  {
          button: 'button_count',
          //url: 'http://d.hatena.ne.jp/pika_shi/',
  });

});
