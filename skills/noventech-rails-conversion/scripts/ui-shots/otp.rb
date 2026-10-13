abort "development only" unless Rails.env.development?
puts User.find_by!(email: "screens@noventech.local").current_otp
