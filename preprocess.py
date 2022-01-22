import preprocessor as p
import re


keywords = ["Coronavirus", "Koronavirus", "Corona", "CDC", "Wuhancoronavirus", "Wuhanlockdown", "Ncov",
            "Wuhan", "N95", "Kungflu", "Epidemic", "outbreak", "Sinophobia", "China", "covid-19", "corona virus",
            "covid", "covid19", "sars-cov-2", "COVID-19", "COVD", "pandemic", "coronapocalypse",
            "canceleverything", "Coronials", "SocialDistancingNow", "Social Distancing", "SocialDistancing",
            "panicbuy", "panic buy", "panicbuying", "panic buying", "14DayQuarantine", "DuringMy14DayQuarantine",
            "panic shop", "panic shopping", "panicshop", "InMyQuarantineSurvivalKit", "panic-buy", "panic-shop",
            "coronakindness", "quarantinelife", "chinese virus", "chinesevirus", "stayhomechallenge", "stay home challenge",
            "sflockdown", "DontBeASpreader", "lockdown", "lock down", "shelteringinplace", "sheltering in place", "staysafestayhome",
            "stay safe stay home", "trumppandemic", "trump pandemic", "flattenthecurve", "flatten the curve", "china virus",
            "chinavirus", "quarentinelife", "PPEshortage", "saferathome", "stayathome", "stay at home", "stay home", "stayhome",
            "GetMePPE", "covidiot", "epitwitter", "pandemie", "wear a mask", "wearamas", "kung flu", "covididiot", "COVID__19"]

keywords = [s.lower() for s in keywords]
keywords = list(set(keywords))


def removeKeywords(tweet):
    # remove URL, Emoji, and Mentions
    p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION)
    tweet = p.clean(tweet)

    tweet = tweet.lower()
    # remove keywords
    for keyword in keywords:
        tweet = tweet.replace(keyword, "")
    tweet = re.sub(" +", " ", tweet)
    return tweet

