# resource "aws_security_group" "yoagent_security_group" {
#   name        = "allow_tls_from_telegram"
#   description = "Allow TLS inbound traffic from telegram Subnets and all outbound traffic"
#   vpc_id      = data.aws_vpc.default_vpc.id
# }
#
# resource "aws_vpc_security_group_ingress_rule" "allow_subnet20_443_only_from_telegram" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "149.154.160.0/20"
#   from_port         = 443
#   ip_protocol       = "tcp"
#   to_port           = 443
# }
#
# resource "aws_vpc_security_group_ingress_rule" "allow_subnet20_80_only_from_telegram" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "149.154.160.0/20"
#   from_port         = 80
#   ip_protocol       = "tcp"
#   to_port           = 80
# }
#
# resource "aws_vpc_security_group_ingress_rule" "allow_subnet20_88_only_from_telegram" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "149.154.160.0/20"
#   from_port         = 88
#   ip_protocol       = "tcp"
#   to_port           = 88
# }
#
# resource "aws_vpc_security_group_ingress_rule" "allow_subnet20_8443_only_from_telegram" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "149.154.160.0/20"
#   from_port         = 8443
#   ip_protocol       = "tcp"
#   to_port           = 8443
# }
#
# resource "aws_vpc_security_group_ingress_rule" "allow_subnet22_443_only_from_telegram" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "91.108.4.0/22"
#   from_port         = 443
#   ip_protocol       = "tcp"
#   to_port           = 443
# }
#
# resource "aws_vpc_security_group_ingress_rule" "allow_subnet22_80_only_from_telegram" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "91.108.4.0/22"
#   from_port         = 80
#   ip_protocol       = "tcp"
#   to_port           = 80
# }
#
# resource "aws_vpc_security_group_ingress_rule" "allow_subnet22_88_only_from_telegram" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "91.108.4.0/22"
#   from_port         = 88
#   ip_protocol       = "tcp"
#   to_port           = 88
# }
#
# resource "aws_vpc_security_group_ingress_rule" "allow_subnet22_8443_only_from_telegram" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "91.108.4.0/22"
#   from_port         = 8443
#   ip_protocol       = "tcp"
#   to_port           = 8443
# }
#
# resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv4         = "0.0.0.0/0"
#   ip_protocol       = "-1"
# }
#
# resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv6" {
#   security_group_id = aws_security_group.yoagent_security_group.id
#   cidr_ipv6         = "::/0"
#   ip_protocol       = "-1"
# }