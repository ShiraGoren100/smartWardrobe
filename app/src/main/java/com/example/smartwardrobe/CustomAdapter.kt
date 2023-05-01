package com.example.smartwardrobe

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.AutoCompleteTextView
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.textfield.TextInputLayout

class CustomAdapter(private val context:Context,private val mList: List<ItemList>) : RecyclerView.Adapter<CustomAdapter.ViewHolder>() {


    // create new views
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        // inflates the card_view_design view
        // that is used to hold list item
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_spinner, parent, false)

        return ViewHolder(view)
    }

    // binds the list items to a view
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val ItemsViewModel = mList[position]
        holder.inputLayout.hint=ItemsViewModel.feature
//        holder.textView.text = ItemsViewModel.text
        val adapter = ArrayAdapter(context, android.R.layout.simple_spinner_dropdown_item, ItemsViewModel.properties)
        holder.textView.setAdapter(adapter)
//        holder.textView.dropDownAnchor = featureInputLayout.id
    }


    // return the number of the items in the list
    override fun getItemCount(): Int {
        return mList.size
    }


    // Holds the views for adding it to image and text
    class ViewHolder(ItemView: View) : RecyclerView.ViewHolder(ItemView) {
        val inputLayout: TextInputLayout = itemView.findViewById(R.id.feature_input)
        val textView: AutoCompleteTextView = itemView.findViewById(R.id.tv_feature)
    }
}