// Isang node; value ang laman at next ang link sa kasunod.
class Node  {
  constructor(value)  {
    this.value=value;
    this.next=null;
  }
}
// Dito naka-track ang head, tail at bilang ng nodes.
class LinkedList  {
// Simulan ang list na walang laman.
  constructor() {
    this.head=null;
    this.tail=null;
    this.size=0;
  }
// Magdagdag ng node sa dulo.
  append(value) {
    const node=new Node(value);
    if(this.tail)this.tail.next=node;
    else this.head=node;
    this.tail=node;
    this.size++;
  }
// Magdagdag ng node sa unahan.
  prepend(value) {
    const node=new Node(value);
    node.next=this.head;
    this.head=node;
    if(!this.tail)this.tail=node;
    this.size++;
  }
// Insert position na nagsisimula sa 1; puwede rin sa gitna ng nodes.
// I-check ang position at ipasok ang node doon; nagsisimula sa 1.
  insertAt(value, position)  {
    if (!Number.isInteger(position) || position < 1 || position > this.size + 1)  {
      throw new Error(`Enter a whole-number position from 1 to ${this.size + 1}.`);
    }
    if (position === 1)  {
      this.prepend(value);
      return;
    }
    if (position === this.size + 1)  {
      this.append(value);
      return;
    }
    let previous = this.head;
    for (let index = 1;
    index < position - 1;
    index++)  {
      previous = previous.next;
    }
    const node = new Node(value);
    node.next = previous.next;
    previous.next = node;
    this.size++;
  }
// Burahin ang unang kaparehong node at ayusin ang links.
  delete(value) {
    let current=this.head,previous=null;
    while(current) {
      if(current.value===value) {
        if(previous)previous.next=current.next;
        else this.head=current.next;
        if(current===this.tail)this.tail=previous;
        this.size--;
        return true;
      }
      previous=current;
      current=current.next;
    }
    return false;
  }
// Hanapin ang value; ibalik ang zero-based index o -1 kung wala.
  search(value) {
    let n=this.head,index=0;
    while(n) {
      if(n.value===value)return index;
      n=n.next;
      index++;
    }
    return -1;
  }
// icollect ang node values bilang array.
  values() {
    let n=this.head,result=[];
    while(n) {
      result.push(n.value);
      n=n.next;
    }
    return result;
  }
// Alisin lahat ng nodes at ibalik ang size sa zero.
  clear() {
    this.head=this.tail=null;
    this.size=0;
  }
}
// Kunin ang form at result element ng kasalukuyang page.
const form=document.querySelector('form'),output=document.getElementById('output');
// Ipakita ang sagot o error message sa result box.
function show(text,error=false) {
  output.textContent=text;
  output.classList.toggle('error',error);
}
// Basahin at i-validate ang numeric input; bawal blank, negative o infinity.
function number(id) {
  const field=document.getElementById(id);
  if(field.value.trim()==='')throw new Error('Please fill in all numbers.');
  const n=Number(field.value);
  if(!Number.isFinite(n)||n<0)throw new Error('Enter a valid number of zero or greater.');
  return n;
}
// Uppercase conversion, triangle area (base × height / 2), o circle area (πr²).
function calculate(kind) {
  try {
    let result;
    if(kind==='uppercase') {
      const value=document.getElementById('text').value;
      if(!value.trim())throw new Error('Please enter some text.');
      result=value.toUpperCase();
    }
    else {
      const area=kind==='triangle'?number('base')*number('height')/2:Math.PI*number('radius')**2;
      if(!Number.isFinite(area))throw new Error('These numbers are too large.');
      result=Number(area.toPrecision(12)).toLocaleString('en-US', {
        maximumFractionDigits:10
      }
      )+' square units';
    }
    show(result);
    return result;
  }
  catch(e) {
    show(e.message,true);
    return e.message;
  }
}
// i-stop ang page reload at kalkulahin ang sagot kapag nagsubmit na ng form.
if(form&&['uppercase','triangle','circle'].includes(form.id))form.addEventListener('submit',event=> {
  event.preventDefault();
  calculate(form.id);
}
);
// Gumawa ng linked list para sa current page session.
const list=new LinkedList();
// I-display ang nodes, arrows at null sa screen.
function render() {
  const container=document.getElementById('nodes');
  container.replaceChildren();
  for(const value of list.values()) {
    const node=document.createElement('span');
    node.className='node';
    node.textContent=value;
    container.append(node);
    const arrow=document.createElement('span');
    arrow.textContent='→';
    container.append(arrow);
  }
  const end=document.createElement('span');
  end.textContent='null';
  container.append(end);
}
// Validate position before changing the list.
// i-run ang napili na work at i-refresh ang display.
function listAction(action,value,position=document.getElementById('position')?.value) {
  if(action==='clear') {
    list.clear();
    show('Your list is empty.');
    render();
    return;
  }
  if(!value.trim()) {
    show('Enter a node value first.',true);
    return;
  }
  if(action==='insert')  {
    try  {
      const raw = String(position ?? '').trim();
      if (!raw) throw new Error('Enter a position first.');
      const target = Number(raw);
      list.insertAt(value, target);
      show(`Inserted “${value}” at position ${target}. ${list.size} nodes in your list.`);
    }
    catch (error)  {
      show(error.message, true);
      return;
    }
  }
  else if(action==='append'||action==='prepend') {
    list[action](value);
    show(`${list.size} node${list.size===1?'':'s'} in your list.`);
  }
  else if(action==='delete')show(list.delete(value)?`Deleted the first node matching “${value}”.`:`“${value}” was not found.`);
  else if(action==='search') {
    const index=list.search(value);
    show(index<0?`“${value}” was not found.`:`Found “${value}” at position ${index+1}.`);
  }
  render();
  return list.values();
}
// Ikabit ang submit at button click events sa linked list actions.
if(form?.id==='linked-list') {
  form.addEventListener('submit',e=> {
    e.preventDefault();
    listAction('append',document.getElementById('value').value);
  }
  );
  form.querySelectorAll('[data-action]').forEach(button=>button.addEventListener('click',()=>listAction(button.dataset.action,document.getElementById('value').value)));
  render();
}
// Optional browser tool integration; mag-register lamang kung supported.
if(form&&['uppercase','triangle','circle','linked-list'].includes(form.id)&&document.modelContext?.registerTool) {
  const lifecycle=new AbortController();
  const fields=form.id==='linked-list'?['action','value']:form.id==='uppercase'?['text']:form.id==='triangle'?['base','height']:['radius'];
  try {
    Promise.resolve(document.modelContext.registerTool( {
      name:form.id==='linked-list'?'modify_linked_list':'compute_'+form.id,title:form.id==='linked-list'?'Modify linked list':'Compute result',description:'Use the visible tool and update its result.',inputSchema: {
        type:'object',properties: {
          ...(form.id==='linked-list'? {
            position: {
              type:'string',description:'Position starting at 1; required for insert.'
            }
          }
          : {
          }
          ),...Object.fromEntries(fields.map(name=>[name,name==='action'? {
            type:'string',enum:['append','prepend','insert','delete','search','clear']
          }
          : {
            type:'string'
          }
          ]))
        }
        ,required:fields,additionalProperties:false
      }
      ,annotations: {
        readOnlyHint:false,untrustedContentHint:true
      }
      ,execute(input) {
        for(const name of fields)if(typeof input[name]!=='string')throw new Error('All fields must be strings.');
        if(form.id==='linked-list') {
          if(!['append','prepend','insert','delete','search','clear'].includes(input.action))throw new Error('Unknown action.');
          document.getElementById('value').value=input.value;
          if(input.action==='insert') {
            if(typeof input.position!=='string')throw new Error('Enter a position.');
            document.getElementById('position').value=input.position;
          }
          listAction(input.action,input.value,input.position);
          return {
            values:list.values(),message:output.textContent
          }
          ;
        }
        for(const name of fields)document.getElementById(name).value=input[name];
        calculate(form.id);
        return {
          result:output.textContent
        }
        ;
      }
    }
    , {
      signal:lifecycle.signal
    }
    )).catch(()=> {
    }
    );
  }
  catch {
  }
  window.addEventListener('pagehide',()=>lifecycle.abort(), {
    once:true
  }
  );
}

/* Controls para sa Queue, Deque at Sorting; Python ang gumagawa ng operations. */
(() => {
  'use strict';
  const byId = id => document.getElementById(id);

  // Result box ang ginagamit sa validation; walang browser popup.
  function status(element, message, error = false) {
    element.textContent = message;
    element.classList.toggle('error', error);
  }

  async function postJSON(endpoint, payload) {
    const response = await fetch(endpoint, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    let result;
    try { result = await response.json(); }
    catch { throw new Error('The server could not return a result. Restart the app and try again.'); }
    if (!response.ok) throw new Error(result.error || 'The operation could not be completed.');
    return result;
  }

  // Bawat page may sariling Tool at Basic info tabs; puwede rin ang keyboard.
  document.querySelectorAll('[data-page-tabs]').forEach(tablist => {
    const tabs = [...tablist.querySelectorAll('[role="tab"][data-panel]')];
    function selectTab(selected) {
      tabs.forEach(tab => {
        const active = tab === selected;
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        byId(tab.dataset.panel).hidden = !active;
      });
      tablist.dispatchEvent(new Event('works-tab-change', { bubbles: true }));
    }
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => selectTab(tab));
      tab.addEventListener('keydown', event => {
        if (!['ArrowRight', 'ArrowLeft', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 :
          (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
        selectTab(tabs[next]);
        tabs[next].focus();
      });
    });
  });

  const structure = document.querySelector('[data-structure]');
  if (structure) {
    const kind = structure.dataset.structure;
    const form = byId('structure-form');
    const field = byId('item-value');
    const message = byId('structure-status');
    let values = [];
    let busy = false;

    function render() {
      const container = byId('structure-items');
      container.replaceChildren();
      values.forEach((value, index) => {
        const item = document.createElement('li');
        item.className = 'wb-item';
        const text = document.createElement('span');
        text.className = 'wb-item-value';
        text.textContent = value;
        const end = document.createElement('span');
        end.className = 'wb-item-end';
        end.textContent = values.length === 1 ? 'FRONT / REAR' : index === 0 ? 'FRONT' : index === values.length - 1 ? 'REAR' : String(index + 1);
        item.append(text, end);
        container.append(item);
      });
      byId('item-count').textContent = String(values.length);
      byId('front-value').textContent = values.length ? values[0] : '—';
      byId('rear-value').textContent = values.length ? values[values.length - 1] : '—';
      byId('is-empty').textContent = values.length ? 'No' : 'Yes';
      byId('empty-state').hidden = values.length > 0;
    }

    async function perform(action) {
      if (busy) return;
      busy = true;
      form.querySelectorAll('button, input').forEach(control => { control.disabled = true; });
      structure.setAttribute('aria-busy', 'true');
      try {
        const result = await postJSON(structure.dataset.endpoint, { action, values, value: field.value });
        values = result.values;
        render();
        status(message, result.message);
        if (['enqueue', 'add_front', 'add_rear', 'clear'].includes(action)) field.value = '';
      } catch (error) {
        status(message, error instanceof TypeError ? 'Unable to reach the app. Check that python app.py is running.' : error.message, true);
      } finally {
        busy = false;
        structure.removeAttribute('aria-busy');
        form.querySelectorAll('button, input').forEach(control => { control.disabled = false; });
        if (['enqueue', 'add_front', 'add_rear'].includes(action)) field.focus();
      }
    }

    form.addEventListener('submit', event => {
      event.preventDefault();
      perform(kind === 'queue' ? 'enqueue' : 'add_rear');
    });
    form.querySelectorAll('[data-operation]').forEach(button => {
      button.addEventListener('click', () => perform(button.dataset.operation));
    });
    render();
  }

  const workbench = byId('sorting-workbench');
  if (!workbench) return;
  const metadata = JSON.parse(byId('sorting-metadata').textContent);
  const form = byId('sorting-form');
  const input = byId('sort-values');
  const algorithm = byId('algorithm');
  const order = byId('sort-order');
  const message = byId('sort-status');
  let trace = null;
  let position = 0;
  let timer = null;
  let busy = false;
  const playback = ['sort-previous', 'sort-play', 'sort-next', 'sort-finish'];

  function pause() {
    if (timer !== null) window.clearInterval(timer);
    timer = null;
    byId('sort-play').textContent = trace && position === trace.steps.length - 1 ? 'Replay' : 'Play';
  }

  function updateInfo() {
    const info = metadata.algorithms[algorithm.value];
    ['name', 'description', 'best', 'average', 'worst', 'space', 'stable', 'note'].forEach(key => {
      byId(`algorithm-${key}`).textContent = info[key];
    });
    byId('algorithm-reference').href = metadata.references.find(reference => reference.id === info.source).url;
  }

  function drawStep() {
    if (!trace) return;
    const step = trace.steps[position];
    const max = Math.max(1, ...trace.original.map(value => Math.abs(value)));
    const bars = step.values.map((value, index) => {
      const bar = document.createElement('div');
      bar.className = 'wb-bar';
      bar.style.minWidth = `${Math.max(32, String(value).length * 8 + 10)}px`;
      bar.classList.toggle('is-active', step.active.includes(index));
      bar.classList.toggle('is-pivot', step.pivot === index);
      bar.classList.toggle('is-done', step.done);
      bar.setAttribute('aria-label', `Position ${index + 1}: ${value}${step.pivot === index ? ', pivot' : ''}`);
      const column = document.createElement('span');
      column.className = 'wb-bar-column';
      column.style.height = `${Math.max(5, Math.abs(value) / max * 70)}%`;
      column.setAttribute('aria-hidden', 'true');
      const label = document.createElement('span');
      label.className = 'wb-bar-label';
      label.textContent = String(value);
      const number = document.createElement('span');
      number.className = 'wb-bar-index';
      number.textContent = String(index + 1);
      bar.append(column, label, number);
      return bar;
    });
    byId('sort-bars').replaceChildren(...bars);
    byId('step-count').textContent = `Step ${position} / ${trace.steps.length - 1}`;
    byId('step-message').textContent = step.message;
    byId('comparison-count').textContent = String(step.comparisons);
    byId('write-count').textContent = String(step.writes);
    byId('sort-previous').disabled = position === 0;
    byId('sort-next').disabled = position === trace.steps.length - 1;
    byId('sort-finish').disabled = position === trace.steps.length - 1;
    byId('sort-play').disabled = false;
    if (position === trace.steps.length - 1 && timer === null) byId('sort-play').textContent = 'Replay';
  }

  function resetTrace(clearInput = false) {
    pause();
    trace = null;
    position = 0;
    byId('sort-play').textContent = 'Play';
    if (clearInput) input.value = '';
    byId('sorted-result').textContent = '—';
    byId('step-count').textContent = 'Step 0 / 0';
    byId('comparison-count').textContent = '0';
    byId('write-count').textContent = '0';
    byId('step-message').textContent = 'Use Next step or Play after sorting.';
    const empty = document.createElement('p');
    empty.className = 'wb-empty';
    empty.textContent = 'Your numbers will appear here.';
    byId('sort-bars').replaceChildren(empty);
    playback.forEach(id => { byId(id).disabled = true; });
    status(message, 'Enter numbers to see the result and its steps.');
  }

  function play() {
    if (!trace) return;
    if (timer !== null) { pause(); return; }
    if (position === trace.steps.length - 1) position = 0;
    byId('sort-play').textContent = 'Pause';
    drawStep();
    timer = window.setInterval(() => {
      position += 1;
      if (position === trace.steps.length - 1) pause();
      drawStep();
    }, Number(byId('sort-speed').value));
  }

  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (busy) return;
    resetTrace();
    busy = true;
    form.querySelectorAll('input, select, button').forEach(control => { control.disabled = true; });
    workbench.setAttribute('aria-busy', 'true');
    status(message, 'Sorting your numbers…');
    try {
      trace = await postJSON(workbench.dataset.endpoint, {
        numbers: input.value, algorithm: algorithm.value, order: order.value
      });
      byId('sorted-result').textContent = trace.result.join('  →  ');
      const info = metadata.algorithms[trace.algorithm];
      status(message, `${info.name} complete · ${trace.result.length} numbers · ${trace.order === 'asc' ? 'ascending' : 'descending'} order. Explore the steps below.`);
      drawStep();
    } catch (error) {
      status(message, error instanceof TypeError ? 'Unable to reach the app. Check that python app.py is running.' : error.message, true);
    } finally {
      busy = false;
      workbench.removeAttribute('aria-busy');
      form.querySelectorAll('input, select, button').forEach(control => { control.disabled = false; });
    }
  });
  input.addEventListener('input', () => resetTrace());
  algorithm.addEventListener('change', () => { updateInfo(); resetTrace(); });
  order.addEventListener('change', () => resetTrace());
  byId('sort-reset').addEventListener('click', () => { resetTrace(true); input.focus(); });
  byId('sort-example').addEventListener('click', () => { resetTrace(); input.value = '8, 3, 5, 1, 4'; input.focus(); });
  byId('sort-previous').addEventListener('click', () => { pause(); if (trace && position > 0) { position -= 1; drawStep(); } });
  byId('sort-next').addEventListener('click', () => { pause(); if (trace && position < trace.steps.length - 1) { position += 1; drawStep(); } });
  byId('sort-finish').addEventListener('click', () => { pause(); if (trace) { position = trace.steps.length - 1; drawStep(); } });
  byId('sort-play').addEventListener('click', play);
  byId('sort-speed').addEventListener('change', () => { if (timer !== null) { pause(); play(); } });
  document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });

  // I-pause ang sorting playback kapag lumipat sa information tab.
  workbench.addEventListener('works-tab-change', pause);
  updateInfo();
})();
