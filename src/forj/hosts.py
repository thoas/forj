from django_hosts import patterns, host


host_patterns = patterns(
    "forj.web",
    host(r"admin", "admin.urls", name="admin"),
    host(r"www", "frontend.urls", name="www"),
)
