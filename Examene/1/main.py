from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers

print("PARTEA 1: Funcții")
print("build_url ('example.com', 'login'):", build_url("example.com", "login"))
print("build_url ('example.com', '/login'):", build_url("example.com", "/login"))
print("is_https ('https://example.com'):", is_https("https://example.com"))
print("is_https ('http://example.com'):", is_https("http://example.com"))

print("\n\nPARTEA 2: Trimiterea unei cereri")
print("--- Caz de succes ---")
show_response("https://example.com")
print("--- Caz de eșec / limită ---")
show_response("http://this-site-does-not-exist.invalid")

print("\n\n PARTEA 3: Un verificator reutilizabil")
print("check_site (succes):", check_site("https://example.com"))
print("check_site (site inexistent):", check_site("http://this-site-does-not-exist.invalid"))

print("\n\nPARTEA 4: Verificarea mai multor site-uri ")
scan_sites()

print("\n\nPARTEA 5: Audit de securitate ")
print("check_headers (https://example.com):", check_headers("https://example.com"))
print("check_headers (site inexistent):", check_headers("http://this-site-does-not-exist.invalid"))