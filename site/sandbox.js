/* Open Family Office — deterministic browser cash budget. MIT. No network or storage. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.OFOCash = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const defaults = Object.freeze({startCash:120000,stableIncome:8000,businessIncome:5000,expenses:10500,drop:0,oneoff:0,eventMonth:6,expenseGrowth:0,eventKind:'windfall'});
  const limits = {startCash:1e9,stableIncome:1e8,businessIncome:1e8,expenses:1e8,drop:100,oneoff:1e9,eventMonth:24,expenseGrowth:50};
  function validate(raw) {
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) throw new TypeError('A budget input object is required.');
    const input = {};
    for (const [key,max] of Object.entries(limits)) {
      const value = raw[key];
      if ((typeof value !== 'number' && typeof value !== 'string') || String(value).trim() === '') throw new TypeError(key + ': enter a number.');
      const n = Number(value);
      if (!Number.isFinite(n) || n < 0 || n > max) throw new RangeError(key + ': value is outside the permitted range.');
      if (['drop','expenseGrowth'].includes(key)) {
        if (Math.abs(n * 100 - Math.round(n * 100)) > 1e-5) throw new RangeError(key + ': maximum two decimal places.');
      } else if (key !== 'eventMonth' && Math.abs(n * 100 - Math.round(n * 100)) > 1e-5) throw new RangeError(key + ': maximum two decimal places.');
      input[key] = n;
    }
    if (!Number.isInteger(input.eventMonth) || input.eventMonth < 1) throw new RangeError('eventMonth: use a whole month from 1 to 24.');
    if (!['windfall','business-sale'].includes(raw.eventKind)) throw new RangeError('eventKind: select windfall or business-sale.');
    input.eventKind=raw.eventKind;
    return input;
  }
  function calculate(raw) {
    const input = validate(raw);
    const cents = n => Math.round(n * 100);
    let cash = cents(input.startCash);
    const stable = cents(input.stableIncome), variable = Math.round(cents(input.businessIncome) * (1-input.drop/100));
    const rows=[]; let firstGap=null,minCash=cash,totalIncome=0,totalExpenses=0;
    for(let m=1;m<=24;m++) {
      const opening=cash;
      const business=input.eventKind==='business-sale'&&m>=input.eventMonth?0:variable;
      const once=m===input.eventMonth?cents(input.oneoff):0;
      const expense=Math.round(cents(input.expenses) * Math.pow(1+input.expenseGrowth/100,Math.floor((m-1)/12)));
      const income=stable+business+once;
      cash=opening+income-expense;
      if(!Number.isSafeInteger(cash)) throw new RangeError('Budget exceeds exact arithmetic bounds.');
      if(cash<0&&firstGap===null)firstGap=m;
      minCash=Math.min(minCash,cash);totalIncome+=income;totalExpenses+=expense;
      rows.push({month:m,opening:opening/100,stable:stable/100,variable:business/100,oneoff:once/100,expenses:expense/100,closing:cash/100});
    }
    return {schema_version:1,model:'24-month nominal cash budget; no investment returns, tax calculation, asset sales or credit assumed',inputs:input,rows,ending_cash:cash/100,minimum_cash:minCash/100,first_gap_month:firstGap,total_inflows:totalIncome/100,total_outflows:totalExpenses/100};
  }
  return Object.freeze({defaults,validate,calculate});
});
