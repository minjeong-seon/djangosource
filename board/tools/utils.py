# ip 가져오는 함수
def get_client_ip(request):
    x_forward_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forward_for:
        ip = x_forward_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
