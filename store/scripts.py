from .models import Product

def productsfromcategory(categories):
   productcontext = []
   for category in categories:
      globals()[category] = category
      print(globals()[category])
      productcontext.append(globals()[category])
   return productcontext
