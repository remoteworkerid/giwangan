class ContentAssistantResultView extends React.Component{
    constructor(props){
      super(props);
      this.state = {
        text: '',
      };
    };

    handleChangeText(event){
      this.setState({url: event.target.value})
    };

    render(){
      return(
        <div>
          <p>{this.props.title}</p>
          <div className="input-group">
            <textarea id="txt_result" className="form-control" value={this.props.text} onChange={this.handleChangeText}></textarea>
          </div>
        </div>
      );
    }
}

var ContentAssistant = React.createClass({

  getInitialState: function() {
    return {
      url: 'http://www.detik.com',
      title: 'Not yet scraped',
      text: 'Not yet scraped',
    };
  },

  handleChange(event){
    this.setState({url: event.target.value})
  },

  render: function(){
    return (
      <div className="input-group">
        <input placeholder="URL" id="txt_url" className="form-control"
        value={this.state.url} onChange={this.handleChange}/>
        <span className="input-group-btn">
          <button className="btn btn-default value-control" id="btn_fetch" onClick={this.onClick}>
          <span className="glyphicon glyphicon-download"></span>
          </button>
        </span>
        <ContentAssistantResultView title={this.state.title} text={this.state.text}/>
      </div>
    );
  },

  handle_scraped_data: function (data, status, jqXHR) {
    data = JSON.parse(data);
    console.log(data);
    this.setState({title: data.result.title});
    this.setState({text: data.result.text});
  },

  onClick: function(){
    console.log('onClick ' + this.state.url);
    $.ajax({
      type: "GET",
      url: "/api/assistant",
      data: {'url': this.state.url},
      dataType: "json",
      success: this.handle_scraped_data,
      error: function (jqXHR, status) {
        console.log(jqXHR);

      }
    });

  },
});

ReactDOM.render(
  <ContentAssistant/>,
  document.getElementById('app_assistant_root')
);