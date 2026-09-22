'use strict';
let language='en',dark=false;
document.getElementById('landingLang').addEventListener('click',()=>{
 language=language==='en'?'zh':'en';
 document.documentElement.lang=language==='zh'?'zh-CN':'en';
 document.querySelectorAll('[data-en][data-zh]').forEach(n=>n.textContent=language==='zh'?n.dataset.zh:n.dataset.en);
 document.getElementById('landingLang').textContent=language==='zh'?'EN':'中文';
});
document.getElementById('landingTheme').addEventListener('click',()=>{dark=!dark;document.documentElement.dataset.theme=dark?'ofo-dark':'ofo';});
