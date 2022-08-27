import logo from './logo.svg';
import React, { Component } from 'react';
import './App.css';
import Status from './components/status'
import axios from 'axios';

const endpoint = '/mine_block'
class App extends Component {
  constructor(props){
    super(props);
  }
  componentWillMount() {
    axios.get(endpoint)
  }
  render(){
  return (
    <div className="App">
    <Status/>
    </div>
    );
  }
}

export default App;