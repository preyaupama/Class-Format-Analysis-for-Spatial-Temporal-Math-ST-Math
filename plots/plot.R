regular_class_data$time <- format(regular_class_data$python_time, format="%H:%M:%S")
regular_class_data$time <- as.POSIXct(regular_class_data$time,format="%H:%M:%S")
regular_class_data$id <- group_indices(regular_class_data,student_entity_id)

# plot(regular_class_data$time, col=regular_class_data$student_entity_id)
# legend(7,4.3,unique(regular_class_data$student_entity_id),col=1:length(regular_class_data$student_entity_id),pch=1)

ggplot(regular_class_data, aes(id, time, colour = id)) + 
  geom_point()


rotation_data$time <- format(rotation_data$python_time, format="%H:%M:%S")
rotation_data$time <- as.POSIXct(rotation_data$time,format="%H:%M:%S")
rotation_data$student <- group_indices(rotation_data,student_entity_id)

ggplot(rotation_data, aes(time, student, colour = student)) + 
  geom_point()


free_seating_data <- subset(lab_DC_2014, iid == 'SIM1JN' & gcd == 'GRADE2' & teacher_entity_id == '168a14954fcb90bd3325f29c4cdb9391844261d98adee91ca363180c2cc84f6b' & session_num_v4 == 16)
free_seating_data$time <- format(free_seating_data$python_time, format="%H:%M:%S")
free_seating_data$time <- as.POSIXct(free_seating_data$time,format="%H:%M:%S")
free_seating_data$student <- group_indices(free_seating_data,student_entity_id)

ggplot(free_seating_data, aes(time, student, colour = student)) + 
  geom_point()



lab_seating_data <- subset(lab_DC_2014, iid == 'LAF1JL' & gcd == 'GRADE4' & teacher_entity_id == '4aeda03c73392cf81e5182cf66b6c617a42a4dc77134a903bbc8f4dbd37c2564' & session_num_v4 == 496)
lab_seating_data$time <- format(lab_seating_data$python_time, format="%H:%M:%S")
lab_seating_data$time <- as.POSIXct(lab_seating_data$time,format="%H:%M:%S")
lab_seating_data$student <- group_indices(lab_seating_data,student_entity_id)

ggplot(lab_seating_data, aes(time, student, colour = student)) + 
  geom_point()

large_class_data <- subset(lab_DC_2014, iid == 'BAN1JL' & gcd == 'GRADE5' & teacher_entity_id == '6b3a7b7fe4d223723ca132927974d933a2e8548adfaf3025c4595a0a55315eff' & session_num_v4 == 503)
large_class_data$time <- format(large_class_data$python_time, format="%H:%M:%S")
large_class_data$time <- as.POSIXct(large_class_data$time,format="%H:%M:%S")
large_class_data$student <- group_indices(large_class_data,student_entity_id)

ggplot(large_class_data, aes(time, student, colour = student)) + 
  geom_point()

long_class_data <- subset(lab_DC_2014, iid == 'HDC1JK' & gcd == 'GRADE4' & teacher_entity_id == '2c1e8f73fa7be44c1a5f1efaf0f44a6511479d2497ee78442652f1f174ad7701' & session_num_v4 == 352)
long_class_data$time <- format(long_class_data$python_time, format="%H:%M:%S")
long_class_data$time <- as.POSIXct(long_class_data$time,format="%H:%M:%S")
long_class_data$student <- group_indices(long_class_data,student_entity_id)

ggplot(long_class_data, aes(time, student, colour = student)) + 
  geom_point()
large_long_class_data <- subset(lab_DC_2014, iid == 'NAL1JL' & gcd == 'GRADE4' & teacher_entity_id == '2bae94c23382cf9806b0fc19f62289f4c0f8af4c99e19feabca511627342355e' & session_num_v4 == 617)
large_long_class_data$time <- format(large_long_class_data$python_time, format="%H:%M:%S")
large_long_class_data$time <- as.POSIXct(large_long_class_data$time,format="%H:%M:%S")
large_long_class_data$student <- group_indices(large_long_class_data,student_entity_id)

ggplot(large_long_class_data, aes(time, student, colour = student)) + 
  geom_point()
