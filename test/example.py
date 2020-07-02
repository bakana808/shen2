
import shen as shenapi
from shen.elo.ranker import RankingMethod

shen = shenapi.init()

a = shen.create_user('A')
b = shen.create_user('B')
c = shen.create_user('C')
d = shen.create_user('D')

tournament = shen.create_tournament('Test', [a, b, c])

m1 = tournament.create_match([a, b])
m1.score[a] = 1
m2 = tournament.create_match([a, c])
m2.score[c] = 1

lb = tournament.generate_leaderboards(RankingMethod)