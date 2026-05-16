import pandas as pd
import requests

API_TOKEN = "60bc20c079aa485c87ec9dd266f20dc5"
BASE_URL = "https://api.football-data.org/v4"

HEADERS = {
    "X-Auth-Token": API_TOKEN,
}

CHAMPIONS_LEAGUE_ID = "CL"

TEAMS = {
    "Arsenal": 57,
    "PSG": 524,
}


def get_team_matches(team_id: int) -> list[dict]:
    url = f"{BASE_URL}/teams/{team_id}/matches"
    params = {"competitions": CHAMPIONS_LEAGUE_ID}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json().get("matches", [])


def matches_to_dataframe(matches: list[dict], team_name: str) -> pd.DataFrame:
    rows = []
    for match in matches:
        rows.append({
            "team": team_name,
            "date": match.get("utcDate"),
            "status": match.get("status"),
            "home_team": match["homeTeam"].get("name"),
            "away_team": match["awayTeam"].get("name"),
            "home_score": match["score"]["fullTime"].get("home"),
            "away_score": match["score"]["fullTime"].get("away"),
            "stage": match.get("stage"),
            "matchday": match.get("matchday"),
        })
    return pd.DataFrame(rows)


def main():
    all_frames = []

    for team_name, team_id in TEAMS.items():
        matches = get_team_matches(team_id)
        df = matches_to_dataframe(matches, team_name)
        all_frames.append(df)

    result = pd.concat(all_frames, ignore_index=True)
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
