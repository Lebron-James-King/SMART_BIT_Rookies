# Explanation
Our team's main idea is to improve the reward function,reward shaping.
## Design the reward of agent
### 1. Static punishment (prevent the vehicle from stopping at the same place)

### 2. Speed penalty (to prevent the vehicle form from being too slow)
𝑣_𝑟𝑒𝑤𝑎𝑟𝑑=𝜈_e−𝑣_𝑡

### 3. Path penalty (to prevent the vehicle from deviating too far from the road center point)
𝑑𝑒𝑣𝑖𝑎𝑡𝑖𝑜𝑛_𝑟𝑒𝑤𝑎𝑟𝑑=𝐸𝑢𝑐𝑙𝑖𝑑𝑒𝑎𝑛𝐷𝑖𝑠𝑡𝑎𝑛𝑐𝑒(𝑝_e,𝑝_c)

### 4. destination penalty (to make the vehicle get rewards in the process of approaching the destination)
𝑑𝑒sti𝑛𝑎𝑡𝑖𝑜𝑛_𝑟𝑒𝑤𝑎𝑟𝑑=𝑀𝑎𝑛ℎ𝑎𝑡𝑡𝑎𝑛𝐷𝑖𝑠𝑡𝑎𝑛𝑐𝑒(𝑝_e,𝑝_𝑡)

### 5. Collision penalty (to prevent vehicles from getting too close to surrounding vehicles)
𝑐𝑜𝑙𝑙𝑖𝑠𝑖𝑜𝑛_𝑟𝑒𝑤𝑎𝑟𝑑=𝐸𝑢𝑐𝑙𝑖𝑑𝑒𝑎𝑛𝐷𝑖𝑠𝑡𝑎𝑛𝑐𝑒(𝑝_e,𝑝_𝑛)

### 6. Intermediate point reward（to prevent traffic from stopping halfway）
When the distance between the vehicle and the destination location is less than a threshold, a certain positive reward will be given at one time.
