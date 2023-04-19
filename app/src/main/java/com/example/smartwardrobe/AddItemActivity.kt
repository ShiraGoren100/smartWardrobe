package com.example.smartwardrobe

import android.content.Intent
import android.graphics.Bitmap

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.view.LayoutInflater
import android.widget.*
import androidx.navigation.ui.AppBarConfiguration
import com.example.smartwardrobe.databinding.ActivityAddItemBinding
import com.google.android.material.textfield.TextInputLayout

class AddItemActivity : AppCompatActivity() {
    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityAddItemBinding
    private lateinit var imageView: ImageView
    private lateinit var propertyMap:MutableMap<String,String>

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
            updateFeatures(features)
        }

        //colors
        val colorInput = findViewById<AutoCompleteTextView>(R.id.tv_color)
        val colors = resources.getStringArray(R.array.colors)
        val colorAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, colors)
        colorInput.setAdapter(colorAdapter)

        binding.btnSave.setOnClickListener(){

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

    private fun updateFeatures(features: Array<String>) {
         lateinit var fname:String
        binding.featureContainer.removeAllViews()
        features?.forEach { feature ->
            val featureInputLayout = LayoutInflater.from(this@AddItemActivity)
                .inflate(R.layout.item_spinner, null) as TextInputLayout

            fname=feature
            featureInputLayout.hint = feature
            val properties = resources.getStringArray(resources.getIdentifier("feature_$feature", "array", packageName))

            val featureAutoCompleteTextView = featureInputLayout.findViewById<AutoCompleteTextView>(R.id.tv_feature)
            val adapter = ArrayAdapter(
                this@AddItemActivity,
                android.R.layout.simple_spinner_dropdown_item,
                properties
            )
            featureAutoCompleteTextView.hint=feature
            featureAutoCompleteTextView.setAdapter(adapter)
            featureAutoCompleteTextView.dropDownAnchor = featureInputLayout.id
            featureAutoCompleteTextView.setOnItemClickListener { parent, view, position, id ->
                val valuek = parent.getItemAtPosition(position).toString()
//                propertyMap[feature]=valuek

                // Use the safe-call operator to access the put method of propertyMap
//                propertyMap?.put(fname, valuek)
            }

            binding.featureContainer.addView(featureInputLayout)
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