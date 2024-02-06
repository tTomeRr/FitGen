resource "aws_lb" "flex_app_alb" {
  name               = "flex-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.allow_http_https.id]
  subnets            = aws_subnet.public_subnets[*].id
 
  enable_deletion_protection = false
}
 
resource "aws_alb_target_group" "flex_alb_tg" {
  name        = "flex-alb-tg"
  port        = 5000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.flex_app_vpc.id
  target_type = "ip"
 
  health_check {
   healthy_threshold   = "5"
   interval            = "30"
   protocol            = "HTTP"
   matcher             = "200"
   timeout             = "5"
   path                = "/"
   unhealthy_threshold = "2"
  }
}

resource "aws_alb_listener" "http" {
  load_balancer_arn = aws_lb.flex_app_alb.id
  port              = 80
  protocol          = "HTTP"
 
  default_action {
   type = "redirect"
 
   redirect {
     port        = 443
     protocol    = "HTTPS"
     status_code = "HTTP_301"
   }
  }
}
 
resource "aws_alb_listener" "https" {
  load_balancer_arn = aws_lb.flex_app_alb.id
  port              = 443
  protocol          = "HTTPS"
 
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.alb_tls_cert_arn
 
  default_action {
    target_group_arn = aws_alb_target_group.flex_alb_tg.id
    type             = "forward"
  }
}