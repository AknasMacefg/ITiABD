db.cameras.insert([
{
  manufacturer: "Canon",
  model: "EOS 5D Mark IV",
  cameraType: "Зеркальная",
  sensorFormat: "Full Frame",
  megapixels: 30.4,
  lens: {
    type: "Body"
  },
  videoResolution: "4096x2160",
  color: "Black",
  country: "Japan",
  opticalZoom: null,
  price: 2500,
  createdAt: new Date()
},
{
  manufacturer: "Nikon",
  model: "D850",
  cameraType: "Зеркальная",
  sensorFormat: "Full Frame",
  megapixels: 45.7,
  lens: {
    type: "Body"
  },
  videoResolution: "3840x2160",
  color: "Black",
  country: "Japan",
  opticalZoom: null,
  price: 2700,
  createdAt: new Date()
},
{
  manufacturer: "Canon",
  model: "EOS R6",
  cameraType: "Беззеркальная",
  sensorFormat: "Full Frame",
  megapixels: 20.1,
  lens: {
    type: "Lens",
    focalLength: 50,
    mount: "RF",
    aperture: 1.8
  },
  videoResolution: "3840x2160",
  color: "Black",
  country: "Japan",
  opticalZoom: 4,
  price: 2200,
  createdAt: new Date()
},
{
  manufacturer: "Nikon",
  model: "D750",
  cameraType: "Зеркальная",
  sensorFormat: "Full Frame",
  megapixels: 24.3,
  lens: {
    type: "Lens",
    focalLength: 50,
    mount: "F",
    aperture: 1.2
  },
  videoResolution: "1920x1080",
  color: "Black",
  country: "Thailand",
  opticalZoom: 3,
  price: 1800,
  createdAt: new Date()
},
{
  manufacturer: "Sony",
  model: "Alpha A7 III",
  cameraType: "Беззеркальная",
  sensorFormat: "Full Frame",
  megapixels: 24.2,
  lens: {
    type: "Body"
  },
  videoResolution: "1920x1080",
  color: "Black",
  country: "Japan",
  opticalZoom: null,
  price: 2000,
  createdAt: new Date()
}
])