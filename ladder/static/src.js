"use strict";
const e = React.createElement;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      players: []
    };
  }

  componentDidMount = () => {
    this.getPlayers();
  };

  getPlayers = async () => {
    // get the players
    const players = await (await fetch("players", {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      }
    })).json();
    // sort by rank
    players.sort((p1, p2) => p1.rank > p2.rank);
    this.setState({ players });
  };

  render() {
    return (
      <table>
        {this.state.players.map((player, i) => {
          return (
            <tr>
              <td>
                <span>{i + 1} - </span>
                <span>
                  {player.first_name} {player.last_name}
                </span>
              </td>
            </tr>
          );
        })}
      </table>
    );
  }
}

const domContainer = document.querySelector("#root");
ReactDOM.render(e(App), domContainer);
