package com.example.smartwardrobe.ui.closet

import androidx.recyclerview.widget.DiffUtil
import com.example.smartwardrobe.data.ClothingItem

class ClothingItemDiffCallback(
    private val oldList: List<ClothingItem>,
    private val newList: List<ClothingItem>
) : DiffUtil.Callback() {

    override fun getOldListSize(): Int {
        return oldList.size
    }

    override fun getNewListSize(): Int {
        return newList.size
    }

    override fun areItemsTheSame(oldItemPosition: Int, newItemPosition: Int): Boolean {
        val oldItem = oldList[oldItemPosition]
        val newItem = newList[newItemPosition]
        // Compare unique identifiers of the items to check if they are the same
        return oldItem.id == newItem.id
    }

    override fun areContentsTheSame(oldItemPosition: Int, newItemPosition: Int): Boolean {
        val oldItem = oldList[oldItemPosition]
        val newItem = newList[newItemPosition]
        // Compare the contents of the items to check if they are the same
        return oldItem == newItem
    }
}
