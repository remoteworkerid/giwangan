var ContentAssistant = React.createClass({

  getInitialState: function() {
    return { url: '' };
  },

  handleChange(event){
    this.setState({url: event.target.value})
  },

  render: function(){
    return (
      <div className="input-group">
        <input placeholder="URL" id="txt_url" className="form-control"
        value={this.state.url} onChange={this.handleChange.bind(this)}/>
        <span className="input-group-btn">
          <button className="btn btn-default value-control" id="btn_fetch" onClick={this.onClick}>
          <span className="glyphicon glyphicon-download"></span>
          </button>
        </span>
      </div>
    );
  },

  onClick: function(){
    console.log('onClick ' + this.state.url);
    $.ajax({
      type: "GET",
      url: "/api/assistant",
      data: {'url': this.state.url},
      dataType: "json",
      success: function (data, status, jqXHR) {
        data = JSON.parse(data);
        console.log(data);
        // TODO create component for each title/text/images for this Assistant
        // BUT Focus on M2 first in the morning yea
        // $('#result').append(data.result.title);
        // text = ' \
        //         <div class="input-group"> \
        //         <textarea id="txt_result" class="form-control">' + data.result.text + '</textarea> \
        //     </div>';
        // $('#result').append(text);

      },

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

/*
 var RandomMessage = React.createClass({
 getInitialState: function() {
 return { message: 'Hello, Universe' };
 },
 onClick: function() {
 var messages = ['Hello, World', 'Hello, Planet', 'Hello, Universe'];
 var randomMessage = messages[Math.floor((Math.random() * 3))];

 this.setState({ message: randomMessage });
 },
 render: function() {
 return (
 <div>
 <MessageView message={ this.state.message }/>
 <p><input type="button" onClick={ this.onClick } value="Change Message"/></p>
 </div>
 );
 }
 });
 */