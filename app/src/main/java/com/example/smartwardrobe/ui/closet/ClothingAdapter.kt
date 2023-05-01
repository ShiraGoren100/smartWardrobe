package com.example.smartwardrobe.ui.closet

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Base64
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.smartwardrobe.R
import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.data.Property
import com.squareup.picasso.Picasso


class ClothingAdapter(private val items: List<ClothingItem>) : RecyclerView.Adapter<ClothingAdapter.ViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_clothing, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = items[position]
        holder.bind(item)
    }

    override fun getItemCount(): Int {
        return items.size
    }

    inner class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val imageView: ImageView = itemView.findViewById(R.id.imageView)
        private val propertiesView: LinearLayout = itemView.findViewById(R.id.clothes)

        fun bind(item: ClothingItem) {
            // Load the image using a library like Picasso or Glide
            Picasso.get().load(item.img).into(imageView)

            // Set the properties
            propertiesView.removeAllViews()
            for (property in item.properties) {
                val propertyView = LayoutInflater.from(itemView.context).inflate(R.layout.item_property, null)
                val titleView: TextView = propertyView.findViewById(R.id.titleView)
                val valueView: TextView = propertyView.findViewById(R.id.valueView)

                titleView.text = property.title
                valueView.text = property.value

                propertiesView.addView(propertyView)
            }
        }
    }
}

