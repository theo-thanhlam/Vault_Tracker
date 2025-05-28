'use server'

import { getClient, PreloadQuery } from "@/lib/apollo-rsc-client"
import {GET_CATEGORY_TREE} from "@/lib/graphql/category/gql"
import { Category } from "@/types/category";


export async function getCategoryTree():Promise<Category | null>{
  const client = await getClient();
  try{
    const {data} = await client.query({query:GET_CATEGORY_TREE})
    console.log(data.category.getAllCategories);
    return data.category.getAllCategories.treeViews

  }catch{
    return null;
  }
}