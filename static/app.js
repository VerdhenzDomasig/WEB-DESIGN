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
if(form&&form.id!=='linked-list')form.addEventListener('submit',event=> {
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
if(form&&document.modelContext?.registerTool) {
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
