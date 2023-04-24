package com.example.smartwardrobe

import android.content.Intent
import android.graphics.Bitmap
import android.graphics.drawable.BitmapDrawable
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.util.Base64
import android.util.Log
import android.view.LayoutInflater
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import androidx.navigation.ui.AppBarConfiguration
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.smartwardrobe.databinding.ActivityAddItemBinding
import com.google.android.material.textfield.TextInputLayout
import com.google.gson.Gson
import okhttp3.internal.notify
import java.io.ByteArrayOutputStream
import java.io.File

class AddItemActivity : AppCompatActivity() {
    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityAddItemBinding
    private lateinit var imageView: ImageView
    private lateinit var propertyMap: MutableMap<String, String>
    private lateinit var lst:ArrayList<ItemList>
    private lateinit var lstAdapter:CustomAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAddItemBinding.inflate(layoutInflater)
        setContentView(binding.root)


        //take a pictur
        imageView = binding.imgView
        imageView.setOnClickListener {
            val takePictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            startActivityForResult(takePictureIntent, 1)
        }
        lst= ArrayList<ItemList>()
        binding.featureContainer.layoutManager=LinearLayoutManager(this)
         lstAdapter=CustomAdapter(this@AddItemActivity,lst)
        binding.featureContainer.adapter=lstAdapter
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

            val base64=convertBitmapToBase64(bitmap)

            propertyMap["img"]=base64
            propertyMap["category"]=binding.tvCategory.text.toString()
            propertyMap["color"]=binding.tvColor.text.toString()

            for (i in 0 until binding.featureContainer.childCount) {
                val view = binding.featureContainer.getChildAt(i)
                if (view is TextInputLayout) {
                    val hint= view.hint.toString()
                    val autoCompleteTextView = view.findViewById<AutoCompleteTextView>(R.id.tv_feature)
                    val text = autoCompleteTextView.text.toString()
                    // Do something with the text
                    propertyMap[hint] = text
                }
            }
            val gson = Gson()
            val json = gson.toJson(propertyMap)


            // Output the JSON string
            println(json)

        }

/*
        binding.tvCategory.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                val selectedCategory = parent?.getItemAtPosition(position).toString()
                val features = featureMap[selectedCategory]
                Snackbar.make(view!!, R.string.app_name, Snackbar.LENGTH_SHORT).show()
                binding.featureContainer.removeAllViews()

                features?.forEach { feature ->
                    val checkBox = CheckBox(this@AddItemActivity)
                    checkBox.text = feature
                    checkBox.layoutParams = LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.WRAP_CONTENT,
                        ViewGroup.LayoutParams.WRAP_CONTENT
                    )
                    binding.featureContainer.addView(checkBox)
                }

            }

            override fun onNothingSelected(parent: AdapterView<*>?) {}
        }
*/
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
/*
            val featureAutoCompleteTextView = featureInputLayout.findViewById<AutoCompleteTextView>(R.id.tv_feature)
            val adapter = ArrayAdapter(this@AddItemActivity, android.R.layout.simple_spinner_dropdown_item, properties)
            featureAutoCompleteTextView.setAdapter(adapter)
            featureAutoCompleteTextView.dropDownAnchor = featureInputLayout.id

            featureAutoCompleteTextView.onItemClickListener = AdapterView.OnItemClickListener { parent, view, position, id ->
//                val parentView = featureAutoCompleteTextView.parent

                val textInputLayout = findViewById<TextInputLayout>(R.id.feature_input)
                val hint = textInputLayout.hint.toString()
                val valuek = parent.getItemAtPosition(position).toString()
                propertyMap[hint] = valuek


            }
*/
            /*  featureAutoCompleteTextView.setOnItemClickListener { parent, view, position, id ->
                  val valuek = parent.getItemAtPosition(position).toString()
  //                fname= featureAutoCompleteTextView.hint.toString()
                  featureInputLayout.hint
                  propertyMap[feature] = valuek

                  // Use the safe-call operator to access the put method of propertyMap
  //                propertyMap?.put(fname, valuek)
              }*/

//            binding.featureContainer.addView(featureInputLayout)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == 1 && resultCode == RESULT_OK) {
            val imageBitmap = data?.extras?.get("data") as Bitmap
            imageView.setImageBitmap(imageBitmap)


        }
    }

}