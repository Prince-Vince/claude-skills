# Development only: a sign-in for the screenshot script (2FA enrolled with a secret the script can read).
abort "development only" unless Rails.env.development?
u = User.find_or_initialize_by(email: "screens@noventech.local")
u.first_name = "Screen"
u.last_name = "Shots"
u.password = u.password_confirmation = "screens-only-#{Rails.application.secret_key_base[0, 12]}"
u.roles = [ "admin" ] if u.respond_to?(:roles=)
u.otp_secret ||= User.generate_otp_secret
u.otp_required_for_login = true
u.save!
client = Client.find_by!("name LIKE ?", "Lakeview%")
puts({ password: u.password, client_id: client.id }.to_json)
