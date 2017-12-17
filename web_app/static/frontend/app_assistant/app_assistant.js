const ce = React.createElement;


const square = ce('div', {
    style: {
        width: '100px',
        height: '100px',
        backgroundColor: 'green',
        margin: '10px'
      }
});

const container = ce('div', {
    style: {
        border: '5px solid green'
        }
    },
    'Rects',
    square,
    square
);

ReactDOM.render(
  container,
  document.getElementById('app_assistant_root')
);
