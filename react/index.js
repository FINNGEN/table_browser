import React from 'react'
import ReactDOM from 'react-dom'
import {
    BrowserRouter,
    Route,
    Switch,
    Link
} from 'react-router-dom'
import { Provider } from 'react-redux'

import store from './store'
import { Table } from './features/Table'

ReactDOM.render(
	<Provider store={store}>
        <BrowserRouter>
        <div style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
        <div style={{flex: 1, height: '100%', padding: '10px', display: 'flex', flexFlow: 'row nowrap', justifyContent: 'flex-start', flexDirection: 'column'}}>
	<Link to='/' style={{paddingBottom: '10px', textDecoration: 'none', color: 'black', width: '200px'}}>FINNGEN CHIP RESULTS</Link>
	<Route path='/' component={Table}/>
        </div>
        </div>
        </BrowserRouter>
	</Provider>
    , document.getElementById('reactEntry'))
