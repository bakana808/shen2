import json
from shen import Shen, _i, _e, _w
from shen.user import User, gen_uuid
from shen.match import Round, Match
from shen.ranker import EloRankingAlgo


def parse_file(file: str):

    _i(f"reading \"{file}\"...")

    shn = Shen()
    ranker = EloRankingAlgo()

    with open(file, "r") as f:
        dct = json.load(f)

        # for k, v in dct.items():
        # _i(f"{k}: {v}")

        _i("populating users...")

        # read users
        for uuid, user_dct in dct["users"].items():

            # try parsing with format 1
            try:
                shn.add_user(User(user_dct["nickname"], id=uuid))
            except Exception:
                pass

            # try parsing with format 2
            try:
                shn.add_user(User(user_dct["displayName"], id=uuid))
            except Exception:
                pass

        _i("populating users (from \"players\")...")

        for uuid, user_dct in dct["players"]["ssb4-s2016"].items():

            if uuid in shn.users:
                _w(f"duplicate user found \"{uuid}\"")

            else:
                shn.add_user(User(uuid, id=uuid))

        i = 0
        for match_id, match_dct in dct["matches"].items():

            user_ids = match_dct["players"]

            _i(f"match {i}: {' vs. '.join(user_ids)}")

            for user_id in user_ids:
                if user_id not in shn.users:
                    _w(f"\tcannot find user {user_id} !")

            rounds = []
            for rnd_dct in match_dct["games"]:
                winner = shn.user(user_ids[rnd_dct["winner"]])
                stage = rnd_dct.get("stage")
                rounds.append(Round([winner]))

            users = [shn.user(uuid) for uuid in user_ids]

            shn.add_match(Match(users=users, rounds=rounds))

            i += 1

    _i("finished reading.")
    _i(f"{len(shn.users)} user(s) found.")

    ranker.start(shn)


if __name__ == "__main__":
    parse_file("club-shen-export.json")
