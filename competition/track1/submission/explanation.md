# Explanation
Our team's main idea is to improve the reward function,reward shaping.
## Design the reward of agent
### 1. Static punishment (prevent the vehicle from stopping at the same place)

### 2. Speed penalty (to prevent the vehicle form from being too slow)
π£_πππ€πππ=π_eβπ£_π‘

### 3. Path penalty (to prevent the vehicle from deviating too far from the road center point)
πππ£πππ‘πππ_πππ€πππ=πΈπ’ππππππππ·ππ π‘ππππ(π_e,π_c)

### 4. destination penalty (to make the vehicle get rewards in the process of approaching the destination)
ππstiπππ‘πππ_πππ€πππ=πππβππ‘π‘πππ·ππ π‘ππππ(π_e,π_π‘)

### 5. Collision penalty (to prevent vehicles from getting too close to surrounding vehicles)
ππππππ πππ_πππ€πππ=πΈπ’ππππππππ·ππ π‘ππππ(π_e,π_π)

### 6. Intermediate point rewardοΌto prevent traffic from stopping halfwayοΌ
When the distance between the vehicle and the destination location is less than a threshold, a certain positive reward will be given at one time.
