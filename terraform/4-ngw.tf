resource "aws_eip" "nat" {
  domain = "vpc"
  tags = {
    Name = "flex_app_eip"
  }
}


resource "aws_nat_gateway" "flex_app_nat" {

  subnet_id     = aws_subnet.public_subnets[0].id
  allocation_id = aws_eip.nat.id

  tags = {
    Name = "flex_app_nat"
  }


  depends_on = [aws_internet_gateway.flex_app_igw]
}