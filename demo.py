import numpy as np

def total_value_size(packing, valus, sizes, max_size):
  # tổng giá trị và trọng lượng của mỗi tổ hợp
  v = 0.0  # tổng giá trị của tổ hợp
  s = 0.0  # tổng trọng lượng của tổ hợp
  n = len(packing)
  for i in range(n):
    if packing[i] == 1:
      v += valus[i]
      s += sizes[i]
  if s > max_size:  # trọng lượng vượt quá giới hạn cho phép
    v = 0.0
  return (v, s)

def adjacent(packing, rnd):
  n = len(packing)
  result = np.copy(packing)
  i = rnd.randint(n)
  if result[i] == 0:
    result[i] = 1
  elif result[i] == 1:
    result[i] = 0
  return result

def solve(n_items, rnd, valus, sizes, max_size, \
  max_iter, start_temperature, alpha):
  # bắt đầu giải quyết bằng Simulated Annealing
  curr_temperature = start_temperature
  curr_packing = np.ones(n_items, dtype=np.int64)
  print("Khởi tạo giá trị ban đầu: ")
  print(curr_packing)

  (curr_valu, curr_size) = \
    total_value_size(curr_packing, valus, sizes, max_size)
  iteration = 0
  interval = (int)(max_iter / 10)
  while iteration < max_iter:
    adj_packing = adjacent(curr_packing, rnd)
    (adj_v, _) = total_value_size(adj_packing, \
      valus, sizes, max_size)

    if adj_v > curr_valu:  # giá trị của tổ hợp mới tốt hơn giá trị của tổ hợp cũ
      curr_packing = adj_packing; curr_valu = adj_v
    else:          # giá trị của tổ hợp mới tệ hơn giá trị của tổ hợp cũ
      accept_p = \
        np.exp( (adj_v - curr_valu ) / curr_temperature ) 
      p = rnd.random()
      if p < accept_p:  # nếu p nhỏ hơn ngưỡng p cho phép thì chấp nhận cả tổ hợp tệ hơn
        curr_packing = adj_packing; curr_valu = adj_v 
      

    if iteration % interval == 0:
      print("Số vòng lặp = %6d : Giá trị = %7.0f : \
        Nhiệt độ = %10.2f " \
        % (iteration, curr_valu, curr_temperature))

    if curr_temperature < 0.00001:
      curr_temperature = 0.00001
    else:
      curr_temperature *= alpha
      
    iteration += 1

  return curr_packing       

def main():
  print("\nBắt đầu Simulated Annealing Demo ")
  print("Tối ưu giá trị của các món đồ với giới hạn trọng lượng là 101.")
  print("Thông tin các món đồ: ")
  items = ["Máy tính", "Thỏi bạc", "Cuốn sách", "Bút máy", "Vòng cổ", "Kim cương", "Bình gốm", "Thỏi vàng", "Bức tranh", "Đồng hồ đeo tay"]
  valus = np.array([79, 32, 47, 18, 26, 85, 33, 40, 45, 59])
  sizes = np.array([85, 26, 48, 21, 22, 95, 43, 45, 55, 52])
  max_size = 101
  
  print("Tên món đồ              Giá trị           Trọng lượng")
  for i in range (0, len(items)):
    space = "";
    for j in range(0, 26 - len(items[i])):
      if j == 24 - len(items[i]) - 7:
        space += "|"
      else:
        space += " "
    print(items[i], end = space)
    print(valus[i], end = '         |        ')
    print(sizes[i])

  rnd = np.random.RandomState(3)  #5
  max_iter = 1000
  start_temperature = 10000.0
  alpha = 0.98

  print("\nCài đặt: ")
  print("Nhiệt độ bắt đầu = %0.1f " \
    % start_temperature)
  print("Alpha = %0.2f " % alpha)

  print("\nBắt đầu giải quyết bài toán ")
  packing = solve(10, rnd, valus, sizes, 
    max_size, max_iter, start_temperature, alpha)
  print("Giải quyết xong ")

  print("\nCác món đồ được chọn bỏ vào ba lô: ")
  print("Tên món đồ              Giá trị           Trọng lượng")
  for i in range (0, len(packing)):
    if packing[i] == 1:
        space = "";
        for j in range(0, 26 - len(items[i])):
          if j == 24 - len(items[i]) - 7:
            space += "|"
          else:
            space += " "
        print(items[i], end = space)
        print(valus[i], end = '         |        ')
        print(sizes[i])
    
  (v,s) = \
    total_value_size(packing, valus, sizes, max_size)
  print("\nTổng giá trị của các món đồ được chọn = %0.1f " % v)
  print("Tổng trọng lượng của các món đồ được chọn = %0.1f " % s)

  print("\nKết thúc demo ")

if __name__ == "__main__":
  main()