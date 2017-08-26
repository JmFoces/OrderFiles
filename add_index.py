import sys
from utils.order.index import  Index

index=Index()

index.put_file(sys.argv[1])