package com.example.smartwardrobe.ui.home

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Base64
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.RecyclerView
import com.example.smartwardrobe.R
import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.ui.closet.ClothingItemDiffCallback
import com.google.android.material.floatingactionbutton.FloatingActionButton

class OutfitAdapter : RecyclerView.Adapter<OutfitAdapter.ViewHolder>() {
    private var items: List<ClothingItem> = emptyList()



    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_outfit, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {

        val item = items[position]
        holder.textView.text = item.id.toString()
//        val base64Image: String = "your_base64_image_here"
        val decodedBytes: ByteArray = Base64.decode(item.img, Base64.DEFAULT)
        val bitmap: Bitmap = BitmapFactory.decodeByteArray(decodedBytes, 0, decodedBytes.size)
        holder.imageView.setImageBitmap(bitmap)

        val propertyStringBuilder = StringBuilder()
        for (property in item.properties) {
            propertyStringBuilder.append(property.title + ": " + property.value).append("\n")
        }
        val propertiesText = propertyStringBuilder.toString()

        holder.propertiesView.text = propertiesText


//        Picasso.get().load(item.img).into(holder.imageView)
//        holder.bind(item)
    }

    override fun getItemCount(): Int {
        return items.size
    }

    fun updateData(newItems: List<ClothingItem>) {
        val diffResult = DiffUtil.calculateDiff(
            ClothingItemDiffCallback(items, newItems)
        )
        items = newItems
        diffResult.dispatchUpdatesTo(this)
    }

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val imageView: ImageView = itemView.findViewById(R.id.img_view)

        val propertiesView: TextView = itemView.findViewById(R.id.properties)
        val textView: TextView = itemView.findViewById(R.id.item_id)

/*
        fun bind(item: ClothingItem) {
            // Load the image using a library like Picasso or Glide
//            Picasso.get().load(item.img).into(imageView)
            textView.text = item.id.toString()
            // Set the properties
//            propertiesView.removeAllViews()
            */
/*  for (property in item.properties) {
                  val propertyView = LayoutInflater.from(itemView.context).inflate(R.layout.item_property, null)
                  val titleView: TextView = propertyView.findViewById(R.id.titleView)
                  val valueView: TextView = propertyView.findViewById(R.id.valueView)

                  titleView.text = property.title
                  valueView.text = property.value

                  propertiesView.addView(propertyView)
              }*//*

        }
*/
    }
}

