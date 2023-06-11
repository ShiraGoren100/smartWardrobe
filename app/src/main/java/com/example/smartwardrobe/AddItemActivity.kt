package com.example.smartwardrobe

import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.drawable.BitmapDrawable
import android.os.Bundle
import android.provider.MediaStore
import android.util.Base64
import android.util.Log
import android.view.LayoutInflater
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.ui.AppBarConfiguration
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.smartwardrobe.databinding.ActivityAddItemBinding
import com.google.android.material.snackbar.Snackbar
import com.google.android.material.textfield.TextInputLayout
import com.google.gson.Gson
import java.io.ByteArrayOutputStream

class AddItemActivity : AppCompatActivity(),RepositoryCallback  {
    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityAddItemBinding
    private lateinit var imageView: ImageView
    private lateinit var propertyMap: MutableMap<String, String>
    private lateinit var lst: ArrayList<ItemList>
    private lateinit var lstAdapter: CustomAdapter
    lateinit var username: String
    lateinit var userid: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAddItemBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.toolbar)

        //take a pictur
        imageView = binding.imgView
        imageView.setOnClickListener {
            val takePictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            startActivityForResult(takePictureIntent, 1)
        }
        lst = ArrayList<ItemList>()
        binding.featureContainer.layoutManager = LinearLayoutManager(this)
        lstAdapter = CustomAdapter(this@AddItemActivity, lst)
        binding.featureContainer.adapter = lstAdapter
        val sharedPreferences = getSharedPreferences("myPrefs", Context.MODE_PRIVATE)
        if (sharedPreferences.contains("name")) {
            username = sharedPreferences.getString("name", null).toString()
            userid = sharedPreferences.getString("id", null).toString()
        }

        //categories
        val categoryInput = findViewById<AutoCompleteTextView>(R.id.tv_category)
        val categories = resources.getStringArray(R.array.categories)
        val categoryAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, categories)
        categoryInput.setAdapter(categoryAdapter)

        val featureMap = mutableMapOf<String, List<String>>()

        categories.forEach { category ->
            val categoryResId = resources.getIdentifier("category_$category", "array", packageName)
            val categor = resources.getStringArray(categoryResId).toList()
            featureMap[category] = categor
        }

        binding.tvCategory.setOnItemClickListener { parent, view, position, id ->
            val category = parent.getItemAtPosition(position).toString()
            val arrayName = "category_$category"
            Log.d("DEBUG", "Category: $category, Array name: $arrayName")
            val features = resources.getStringArray(
                resources.getIdentifier(arrayName, "array", packageName)
            )
            propertyMap = mutableMapOf<String, String>()
            lst.clear()
            updateFeatures(features)
        }

        //colors
        val colorInput = findViewById<AutoCompleteTextView>(R.id.tv_color)
        val colors = resources.getStringArray(R.array.colors)
        val colorAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, colors)
        colorInput.setAdapter(colorAdapter)

        binding.btnSave.setOnClickListener() {
            val bitmap = (imageView.drawable as BitmapDrawable).bitmap

            val base64 = convertBitmapToBase64(bitmap)

            propertyMap["img"] = base64
            propertyMap["category"] = binding.tvCategory.text.toString()
            propertyMap["color"] = binding.tvColor.text.toString()

            for (i in 0 until binding.featureContainer.childCount) {
                val view = binding.featureContainer.getChildAt(i)
                if (view is TextInputLayout) {
                    val hint = view.hint.toString()
                    val autoCompleteTextView = view.findViewById<AutoCompleteTextView>(R.id.tv_feature)
                    val text = autoCompleteTextView.text.toString()
                    // Do something with the text
                    propertyMap[hint] = text
                }
            }
            val gson = Gson()
            val json = gson.toJson(propertyMap)

            val rep = AddRepository(this)
            rep.addItem(userid,json)
            // Output the JSON string
            println(json)

        }

    }

    fun convertBitmapToBase64(bitmap: Bitmap): String {
        val outputStream = ByteArrayOutputStream()
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, outputStream)
        val byteArray = outputStream.toByteArray()
        return Base64.encodeToString(byteArray, Base64.DEFAULT)
    }

    private fun updateFeatures(features: Array<String>) {
        lateinit var fname: String
        binding.featureContainer.removeAllViews()
        features?.forEach { feature ->
            val featureInputLayout = LayoutInflater.from(this@AddItemActivity)
                .inflate(R.layout.item_spinner, null) as TextInputLayout

            fname = feature
            featureInputLayout.hint = feature
            val properties = resources.getStringArray(resources.getIdentifier("feature_$feature", "array", packageName))

            lst.add(ItemList(feature, properties.toList()))
            lstAdapter.notifyDataSetChanged()

        }
    }

    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == 1 && resultCode == RESULT_OK) {
            val imageBitmap = data?.extras?.get("data") as Bitmap
            imageView.setImageBitmap(imageBitmap)


        }
    }

    override fun onSuccess() {
        Snackbar.make(binding.btnSave, R.string.success, Snackbar.LENGTH_LONG)
            .setAction("Action", null).show()

        finish()
    }

    override fun onError(message: String) {
        Snackbar.make(binding.btnSave, R.string.failure, Snackbar.LENGTH_LONG)
            .setAction("Action", null).show()
        finish()
    }

}