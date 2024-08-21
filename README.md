# Background

I've previously used various statistical and probabilistic methods to predict New Zealand's Lotto. In 2022, I also attempted predictions using machine learning and deep learning techniques.

Although we rationally know that Lotto is unpredictable, as a tech guy with a background in mathematics and computer science, I can't help but try to find patterns.

This time, I'm using a simple statistical method for prediction.

# Method

We all know about Markov processes, so I considered each draw as being dependent only on the previous one. 

Admittedly, this assumption is quite a stretch, considering there's usually a gap of several days between draws, and they are essentially independent.

Still, we can't treat one draw as a state to predict the next.

My algorithm records the 8 balls in each drawn as follows: B1, B2, B3, B4, B5, B6, BB (Bonus Ball), and PB (Power Ball). For simplicity, I'll refer to B1 through B6 as Bn.

I linked each number from the previous draw with the 7 numbers from the next draw (excluding the Bonus Ball), and then accumulated the results. For example, if this draw yielded (B1, B2, B3, B4, B5, B6, BB, PB) and the next draw yielded (B1-N, B2-N, B3-N, B4-N, B5-N, B6-N, BB-N, PB-N), I would record (B1, B1-N) as 1, (B1, B2-N) as 1, and so on.

I calculated the following relationships: Bn - Bn, Bn - PB, BB - Bn, BB - PB, PB - Bn, and PB - PB.

After iterating through all the data, I obtained some historical data. I summed up all the predictions for Bn and all the predictions for PB to generate a total ranking, representing the likelihood of numbers appearing in the next draw.

I then analyzed the historical data for Bn and PB when pairs of numbers appeared together in a single draw, focusing on the relationships between these pairs: Bn - Bn and Bn - PB. I also calculated the total ranking for these pairs.

# Conclusion

As expected, it's impossible to predict the Lotto, not even for a Division 7 prize.
