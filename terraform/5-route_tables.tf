resource "aws_route_table" "public_rt" {

  vpc_id = aws_vpc.flex_app_vpc.id

  route {

    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.flex_app_igw.id

  }

  tags = {

    Name = "Public Route Table"

  }


}

resource "aws_route_table" "private_rt" {

  vpc_id = aws_vpc.flex_app_vpc.id

  route {

    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.flex_app_nat.id

  }

  tags = {

    Name = "Private Route Table"

  }


}

resource "aws_route_table_association" "public_subnet_asso" {

  count = length(var.public_subnet_cidrs)

  subnet_id = element(aws_subnet.public_subnets[*].id, count.index)

  route_table_id = aws_route_table.public_rt.id

}

resource "aws_route_table_association" "private_subnet_asso" {

  count = length(var.private_subnet_cidrs)

  subnet_id = element(aws_subnet.private_subnets[*].id, count.index)

  route_table_id = aws_route_table.private_rt.id

}