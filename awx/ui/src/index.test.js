import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

jest.mock('react-dom', () => ({ render: jest.fn() }));
jest.mock('util/webWorker', () => jest.fn());

describe('index.jsx', () => {
  it('renders ok', () => {
    const div = document.createElement('div');
    div.setAttribute('id', 'app');
    document.body.appendChild(div);
    require('./index.js'); // eslint-disable-line global-require
    expect(ReactDOM.render).toHaveBeenCalledWith(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
      div
    );
  });
});
