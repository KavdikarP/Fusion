import google.auth

credentials, project = google.auth.default()
print(f"Project: {project}")