import json
import shen
from shen.user import User, gen_uuid
from shen.match import Round, Match
from shen.ranker import EloRankingAlgo

_i, _w, _e = shen._i, shen._w, shen._e


def parse_file(file: str):

    _i(f"reading \"{file}\"...")

    shn = shen.init()
    ranker = EloRankingAlgo()

    with open(file, "r") as f:
        dct = json.load(f)

        # for k, v in dct.items():
        # _i(f"{k}: {v}")

        _i("populating users...")

        # read users
        for uuid, user_dct in dct["users"].items():

            user = None

            # try parsing with format 1
            try:
                user = shn.add_user(User(user_dct["nickname"], uuid=uuid))
            except Exception:
                pass

            # try parsing with format 2
            try:
                user = shn.add_user(User(user_dct["displayName"], uuid=uuid))
            except Exception:
                pass

            if user:
                print(f"\t{user}")

        _i("populating tournaments...")
        for tny_id, players_dct in dct["players"].items():

            tny = shn.create_tournament(title=tny_id)

            for uuid, player_dct in players_dct.items():
                nickname = player_dct.get("nickname")
                try:
                    tny.add_user(shn.user(uuid), nickname=nickname)
                except Exception:
                    _w(f"\tuser \"{uuid}\" does not exist, creating one...")
                    user = shn.add_user(User(uuid, uuid=uuid))
                    tny.add_user(shn.user(uuid), nickname=nickname)

            i = 0
            for match_id, match_dct in dct["matches"].items():

                user_ids = match_dct["players"]

                _i(f"match {i}: {' vs. '.join(user_ids)}")

                for user_id in user_ids:
                    if user_id not in shn.users:
                        _w(f"\tcannot find user {user_id} !")

                users = [shn.user(uuid) for uuid in user_ids]
                match = tny.start_match(users=users)

                for rnd_dct in match_dct["games"]:
                    winner = shn.user(user_ids[rnd_dct["winner"]])
                    rnd = match.record_win(winner)
                    rnd.meta["stage"] = rnd_dct.get("stage")

                i += 1

    _i("finished reading.")
    _i(f"{len(shn.users)} user(s) found.")

    ranker.start(tny)


if __name__ == "__main__":
    parse_file("club-shen-export.json")
