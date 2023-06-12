package com.example.smartwardrobe.ui.closet

import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter

import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.smartwardrobe.MainActivity

import com.example.smartwardrobe.R
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.data.Property
import com.example.smartwardrobe.data.model.LoggedInUser
import com.example.smartwardrobe.databinding.FragmentClosetBinding
import com.google.android.material.snackbar.Snackbar
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.ResponseBody
import okhttp3.internal.notify
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ClosetFragment : Fragment() {

    private var _binding: FragmentClosetBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!
    private lateinit var items: ArrayList<ClothingItem>
    private lateinit var itemsAdapter: ClothingAdapter

    @SuppressLint("NotifyDataSetChanged")
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,

        savedInstanceState: Bundle?
    ): View {
        val closetViewModel =
            ViewModelProvider(this).get(ClosetViewModel::class.java)

        _binding = FragmentClosetBinding.inflate(inflater, container, false)
        val root: View = binding.root

        items = ArrayList<ClothingItem>()

        binding.clothes.layoutManager = LinearLayoutManager(activity)
        itemsAdapter = ClothingAdapter()
        binding.clothes.adapter = itemsAdapter

        itemsAdapter.setOnDeleteClickListener { position ->

            val deletedItem = items[position]
            Snackbar.make(binding.clothes, deletedItem.id.toString(), Snackbar.LENGTH_LONG)
            deleteFromDB(deletedItem.id)
            items.removeAt(position)

            itemsAdapter.notifyItemRemoved(position)
        }

        val categoryInput = binding.tvCategory
        val categories = resources.getStringArray(R.array.categories)
        val categoryAdapter = context?.let { ArrayAdapter(it, android.R.layout.simple_list_item_1, categories) }
        categoryInput.setAdapter(categoryAdapter)
//        categories.forEach { category ->
//            val categoryResId = resources.getIdentifier("category_$category", "array", packageName)
//            val categor = resources.getStringArray(categoryResId).toList()
//        }

        binding.tvCategory.setOnItemClickListener { parent, view, position, id ->
            val category = parent.getItemAtPosition(position).toString()
            val arrayName = "category_$category"
            Log.d("DEBUG", "Category: $category, Array name: $arrayName")
            val features = resources.getStringArray(
                resources.getIdentifier(arrayName, "array", requireActivity().packageName)
            )
            items.clear()

            lifecycleScope.launch {
                val clothingItemList = getList("$category")

                // Handle the returned clothingItemList
                if (clothingItemList != null) {
                    items = clothingItemList
                    itemsAdapter.notifyDataSetChanged()
                    val newItems: List<ClothingItem> = items
                    itemsAdapter.updateData(newItems)
                    // The API call was successful, process the list of clothing items
                    // e.g., Update UI, populate RecyclerView, etc.
                } else {
                    // There was an error or the response was not successful
                    // Handle the error case
                }
            }

        }

//        val textView: TextView = binding.textGallery
//        closetViewModel.text.observe(viewLifecycleOwner) {
//            textView.text = it
//        }
        return root
    }

    private fun deleteFromDB(id: Int) {
        var retrofit = RetrofitClient.myApi

        /*val call = retrofit.deleteItem(id)
        call.enqueue(object : Callback<ResponseBody> {
            override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                // handle successful response
                Snackbar.make(binding.clothes, "id", Snackbar.LENGTH_LONG)

            }

            override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                // handle error
            }
        })*/

        lifecycleScope.launch(Dispatchers.IO) {
            try {
                val response = retrofit.deleteItem(id).execute()
                if (response.isSuccessful) {
                    // Item deleted successfully
                    // Handle any necessary operations after deletion
                } else {
                    // Handle error response
                    val errorBody = response.errorBody()
                    // Process error body if needed
                }
            } catch (e: Exception) {
                // Handle exception
                e.printStackTrace()
            }
        }
    }

    private suspend fun getList(category: String): ArrayList<ClothingItem>? {
        var retrofit = RetrofitClient.myApi
        val queryParameters = mapOf("id" to (activity as MainActivity).userid, "category" to category)

        return withContext(Dispatchers.IO) {
            try {
                val response = retrofit.getCloset(queryParameters).execute()
                if (response.isSuccessful) {
                    val lst = response.body()
                    lst as ArrayList<ClothingItem> // Cast the response to ArrayList<ClothingItem>
                } else {
                    null // Return null or handle the error case appropriately
                }
            } catch (e: Exception) {
                print(e)
                null // Return null or handle the exception case appropriately
            }
        }
        itemsAdapter.notifyDataSetChanged()
    }

/*
    private fun getList(category: String): ArrayList<ClothingItem> {
        val dataStr =
            """[{ "id":"1", "img": "string", "category": "Shirts", "color": "blue", "Sleeves": "Sleeveless", "Weather": "Heat wave", "Thickness": "Light" }, { "id":2, "img": "string", "category": "Shirts", "color": "blue", "Sleeves": "Sleeveless", "Weather": "Heat wave", "Thickness": "Light" }, { "id":3, "img": "string", "category": "Shirts", "color": "blue", "Sleeves": "Sleeveless", "Weather": "Heat wave", "Thickness": "Light" }]"""
        val gson = Gson()
        val data = gson.fromJson(dataStr, Array<Map<String, String>>::class.java).toList()
        return data.map { map ->
            ClothingItem(
                map["id"]!!.toInt(),
                map["img"]!!,
                listOf(
                    Property("category", map["category"]!!),
                    Property("color", map["color"]!!),
                    Property("Sleeves", map["Sleeves"]!!),
                    Property("Weather", map["Weather"]!!),
                    Property("Thickness", map["Thickness"]!!)
                )
            )
        }.toCollection(ArrayList())
    }
*/


    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}