from __future__ import unicode_literals

import redis

# my server
HOST = "redis-19723.c61.us-east-1-3.ec2.cloud.redislabs.com"
PWD = "15235021453.ljhX"
PORT = "19723"
r = redis.Redis(host=HOST, password=PWD, port=PORT)

# add information in the database
dic = {
    "coronavirus":
    "Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2), previously known by the provisional name 2019 novel coronavirus (2019-nCoV),is a positive-sense single-stranded RNA virus. It is contagious in humans and is the cause of the ongoing 2019 coronavirus pandemic, an epidemic of coronavirus disease 2019 (COVID-19) that has been designated a Public Health Emergency of International Concern by the World Health Organization (WHO). SARS-CoV-2 has close genetic similarity to bat coronaviruses, from which it likely originated. An intermediate reservoir such as a pangolin is also thought to be involved in its introduction to humans. From a taxonomic perspective SARS-CoV-2 is classified as a strain of the species severe acute respiratory syndrome-related coronavirus (SARSr-CoV). The strain was first discovered in Wuhan, China.           ---source from: wikipedia.com",
    "measurements":
    "There are usually two strategies for detecting infectious diseases: detecting the pathogen itself, or detecting antibodies produced by the body in order to resist the pathogen. Detection of pathogens can detect both antigens (generally pathogen surface proteins, and some use internal nuclear proteins), as well as nucleic acids. If any of the antibodies, antigens, or nucleic acids is detected in the patient's body fluids, it means that they are infected. Because antibodies take time to produce, generally ranging from a few days to a few weeks, some patients with weak immune functions may have low antibody levels, which can easily cause false negatives (already infected, but the test results do not appear to be infected). At the beginning of the infection, the pathogen antigen content is also low, and it is also not easy to detect. Therefore, it is currently widely used to detect the nucleic acid sequence of a pathogen, and the signal is amplified by an amplification reaction, and the detection has high sensitivity and specificity.              ---source from: thepaper.cn",
    "symptoms":
    "People infected with COVID-19 may have mild or no symptoms. You may not know that you have the symptoms of Coronavirus Diseas (COVID-19) 2019 because they are similar to a cold or flu. Symptoms can take up to 14 days, which is the longest known infection period of the virus.The main syptoms may contains: fever, cough, Difficulty breathing, Pneumonia in both lungs, etc.            ---source from: canada.ca",
    "pictures": ""
}
for i in dic.keys():
    r.set(i, dic[i])


# 如果键入就测试
def basic_measure():
    # use for self-testing
    while True:
        print("*" * 100)
        print("Welcome to use self-measurement".center(100, '-'))
        print("*" * 100)
        x = int(
            input(
                "Have you ever been in China in last 14 days?       0(No)/1(Yes):"
            ))
        y = int(
            input(
                "Have you meet people who from China?         0(No)/1(Yes):"))
        z = int(
            input(
                "Do you have any syptoms? Such as fever, cough, Difficulty breathing, etc.          0(No)/1(Yes):"
            ))
        weight = [0.2, 0.3, 0.5]
        # score threshold, if larger than this value, consider the user has high possiblity to have the coronavirus.
        threshold = 0.7
        score = weight[0] * x + weight[1] * y + weight[2] * z
        if score >= threshold:
            print()
            print("-" * 100)
            print("| You need to go to the hospital as soon as possible. |".
                  center(100, ' '))
            print("-" * 100)
        else:
            if x == 1 or y == 1:
                print()
                print("-" * 100)
                print(" You should stay in your house for 14 days. ")
                print("-" * 100)
        print("Thanks for using this simple self measurement.".center(
            100, "-"))
        print("*" * 100)
        b = int(input("Press '1' to quit, '0' for testing again."))
        if b == 1:
            break


while True:
    msg = input(
        "Please enter your query (type 'quit' or 'exit' to end):").strip()
    if msg == 'quit' or msg == 'exit':
        print("Program ends")
        break
    elif msg == '':
        continue
    # provide basic measurements for users
    elif msg == 'basic measurements':
        basic_measure()

    # Add your code here
    else:
        # if the input is not in the database, return string
        # Provide key search.
        # If keyword appear in a sentence, return the answer.
        for i in msg.split():
            if i in r.keys():
                value = r.get(i)
                # count = r.incr(msg, amount=1)
                print(value)
            else:
                continue
    # print("you have entered " + msg + " for " + str(count) + " times")
