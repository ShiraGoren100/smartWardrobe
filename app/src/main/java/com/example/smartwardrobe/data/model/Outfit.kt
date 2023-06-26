package com.example.smartwardrobe.data.model

import com.example.smartwardrobe.data.ClothingItem

data class Outfit(val outfitId: Int, val date: String, val list: ArrayList<ClothingItem>, val userId: String)
