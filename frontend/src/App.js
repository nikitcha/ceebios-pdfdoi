import './App.css';
import React from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';


const palette = {
  "title":'rgb(251, 32, 86)',
  "o":'rgb(100,100,100)'
}


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {'page':0, 'data':{'tokens':[], 'page':'', 'title':'', 'annotated':0}, 'selected_class':'o', 'selected_words':[]};
  }

  onClickPrev () {
    var newpage = Math.max(0,this.state.page-1)
    this.setState({'page':newpage})
    axios.get('http://127.0.0.1:8000/api/page/'+newpage)
        .then(response => response.data)
        .then(data => {
          this.setState({'data':data});
      })        
  }

  async onClickNext () {
    var newpage = this.state.page+1
    this.setState({'page':newpage})
    let res = await axios.get('http://127.0.0.1:8000/api/page/'+newpage);
    let data = res.data;
    this.setState({'data':data});
  }  

  onClickGo () {
    var el = document.getElementById('page');
    this.setState({'page':Number(el.value)})
    axios.get('http://127.0.0.1:8000/api/page/'+this.state.page)
        .then(response => response.data)
        .then(data => {
          this.setState({'data':data});
      })
  }

  onClickClass(e) {
    this.setState({'selected_class':e.target.outerText})
  }
 
  onClickReset() {    
    let a = this.state; //creates the clone of the state
    for (let i=0; i<a.data.tokens.length; i++) {
      a.data.tokens[i].class = 'o'
    }
    this.setState(a);
    axios.post("http://127.0.0.1:8000/api/reset", {"id":a.page,"tokens":a.data.tokens, "classes":[]})
    .then(response => {
      console.log(response.data);
    })        
  }  

  onClickSave() {
    const params = {"id":this.state.page,"tokens":this.state.data.tokens, "classes":[]} //
    axios.post("http://127.0.0.1:8000/api/save", params)
    .then(response => {
      console.log(response.data);
    })    
  }

  onClickGetDois() {
    axios.post("http://127.0.0.1:8000/api/dois")
  }

  onClickTokens() {
    axios.post("http://127.0.0.1:8000/api/tokens");
  }

  onClickConvert() {
    axios.post("http://127.0.0.1:8000/api/convert");
  }

  renderWords() {
    var arr = []
    var color
    var border
    for (let i=0; i<this.state.data.tokens.length; i+=1) {
      border = "0px";
      if (this.state.data.tokens[i].class==="o") {
        color = palette[this.state.data.tokens[i].class];        
      }        
      else {
        color = palette[this.state.data.tokens[i].class.substring(2)];
        if (this.state.data.tokens[i].class.slice(0,2)==='b-') {
          border="1px solid"
        } else if (this.state.data.tokens[i].class.slice(0,2)==='e-') {
          border="1px dashed"
        }
      }
      arr.push(
        <span id={i} key={i}
        style={{"whiteSpace":"pre-wrap", 'color':color, 'border':border,"borderRadius":"4px"}}>
          {this.state.data.tokens[i].text+" "}
        </span>
      )
    }
    return arr
  }

  componentDidUpdate() {
    var counter = document.getElementById('page');
    counter.value = this.state.page;    
    console.log(this.state)
  }  
  
  renderClasses () {
    var arr = [];      
    var border
    for (var key in palette) {
      if (key===this.state.selected_class) {
        border = '4px solid'
      } else {
        border = '2px solid'
      }
      arr.push(
          <span id={key} key={key} onClick={(e)=>this.onClickClass(e)} style={{
            'color':palette[key],
            'border':border,
            'borderRadius':'5px',
            'margin':'5px',
            'padding':'1px'
          }}>{key}</span>
      );
    }
    return arr
  }

  getSelection(e) {
    var sclass
    let sel = window.getSelection()
    let startid = Number(sel.baseNode.parentNode.id)
    let endid = Number(sel.focusNode.parentNode.id)
    let a = this.state.data
    for (let i=startid; i<=endid; i+=1) {
      if ((e.buttons===0) && (this.state.selected_class!=="o")){
        switch(i) {
          case startid:
            sclass = 'b-'+ this.state.selected_class;
            break;
          case endid:
            sclass = 'e-'+ this.state.selected_class;
            break;
          default:
            sclass = 'i-'+ this.state.selected_class;
        }
        a.tokens[i].class = sclass;
      } else {
        a.tokens[i].class = "o";
      }
    }
    this.setState({data: a});
  }  

  render() {
    return (
      <div className="App">
        <div className="App list-group-item" 
        style={{"width":"380px","marginTop":"10px","marginLeft":"10px", "backgroundColor":"white",'zIndex':'1', 'position':'fixed', 'height':"400px"}}>
          <div style={{'margin':'10px'}}>
            File Actions: 
            <button className="btn btn-primary mx-1" onClick={()=>this.onClickConvert()}>PDF to JSON</button>
            <button className="btn btn-success mx-1" onClick={()=>this.onClickTokens()}>Tokenize</button>
          </div>
          <div style={{'margin':'10px'}}>
            Doc Number: <input className="mb-1" placeholder="0" id='page' style={{'width':"30px",'marginRight':"10px"}}/>
          </div>
          <div style={{'margin':'10px'}}>
            Doc Title: <div id='doc-title'>{this.state.data.title}</div>
          </div>
          <div style={{'marginTop':'10px'}}>
            Doc Actions: 
            <button className="btn btn-success mx-1" onClick={()=>this.onClickGo()}>Fetch</button>
            <button className="btn btn-info mx-1" onClick={()=>this.onClickPrev()}>Prev</button>
            <button className="btn btn-primary mx-1" onClick={()=>this.onClickNext()}>Next</button>
          </div>
          <div style={{'marginTop':'10px'}}>
            Annotations:
            <button className="btn btn-secondary mx-1" onClick={()=>this.onClickSave()}>Save</button>
            <button className="btn btn-danger mx-1"onClick={()=>this.onClickReset()}>Reset</button>
          </div>
          <div style={{'marginTop':'10px'}}>
            <button className="btn btn-primary mx-1" onClick={()=>this.onClickGetDois()}>Export DOIs</button>
          </div>
          <div id="container-classes" style={{"width":"100%","marginTop":"20px","backgroundColor":"white"}}>
            <span>Select Class: </span>
            { this.renderClasses() }
          </div>
        </div>
        <div id="container-words" onMouseUp ={(e)=>this.getSelection(e)} style={{"width":"800px","marginTop":"20px", "marginLeft":"400px",'position':'absolute','zIndex':'0'}}>
            { this.renderWords() }
          </div>
      </div>
    );    
  }
}

export default App;
