"use strict";
const e = React.createElement;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      players: [],
      games: []
    };
  }

  componentDidMount = () => {
    this.getPlayers();
    this.getGames();
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

  getGames = async () => {
    const games = await (await fetch("games", {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      }
    })).json();
    this.setState({ games });
  };

  render() {
    return (
      <div>
        <h2>Ranks</h2>
        <table>
          {this.state.players.map((player, i) => {
            return (
              <tr>
                <td>
                  <img src={player.image_url} width={100} />
                  <span>{i + 1} - </span>
                  <span>{player.name} - </span>
                  <span>
                    ({player.wins}-{player.losses}-{player.ties})
                  </span>
                </td>
              </tr>
            );
          })}
        </table>
        <h2>Games</h2>
        <table>
          {this.state.games.map((game, i) => {
            let player_a = game["players"][0];
            let player_b = game["players"][1];
            return (
              <tr>
                <td>
                  <span>{game.date} - </span>
                  <span>
                    {player_a.player.name} ({player_a.score})
                  </span>
                  <span> v. </span>
                  <span>
                    {player_b.player.name} ({player_b.score})
                  </span>
                </td>
              </tr>
            );
          })}
        </table>
      </div>
    );
  }
}

const domContainer = document.querySelector("#root");
ReactDOM.render(e(App), domContainer);
