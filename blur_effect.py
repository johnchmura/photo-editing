from tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import math

class RadialBlurUI:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Blur Controller")
        
    
        self.original_image = Image.open(image_path).convert("RGB")
        self.width, self.height = self.original_image.size
        
        
        self.focal_point = (self.width // 2, self.height // 2)
        self.max_blur = 5
        self.radius = 100  # Circle radius
        
        
        self.blur_mode = StringVar(value="radial")  # "radial" or "linear"
        self.line_point = (self.width // 2, self.height // 2)
        self.line_angle = 0   # in degrees 
        self.line_band = 50   # thickness of the band
        
       
        self.preview_scale = 0.5
        self.preview_image = self.original_image.resize(
            (int(self.width * self.preview_scale), int(self.height * self.preview_scale))
        )
        self.tk_image = ImageTk.PhotoImage(self.preview_image)
        
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        
        self.canvas = Canvas(self.root, 
                             width=self.preview_image.width, 
                             height=self.preview_image.height)
        self.canvas.pack(side=LEFT, padx=10, pady=10)
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)
        
        self.canvas.bind("<B1-Motion>", self.drag_event)
        self.canvas.bind("<Button-1>", self.drag_event)
        
        
        control_frame = Frame(self.root)
        control_frame.pack(side=RIGHT, padx=10, pady=10)
        
        
        Label(control_frame, text="Blur Mode:").pack(anchor=W)
        modes_frame = Frame(control_frame)
        modes_frame.pack(anchor=W)
        Radiobutton(modes_frame, text="Radial", variable=self.blur_mode, value="radial", 
                    command=self.update_display).pack(side=LEFT)
        Radiobutton(modes_frame, text="Linear", variable=self.blur_mode, value="linear", 
                    command=self.update_display).pack(side=LEFT)
        
       
        Label(control_frame, text="Focal Radius (Radial Mode)").pack(anchor=W)
        self.radius_slider = Scale(control_frame, from_=10, to=500, orient=HORIZONTAL, 
                                   command=self.update_radius)
        self.radius_slider.set(self.radius)
        self.radius_slider.pack(fill=X)
        
       
        Label(control_frame, text="Line X (Linear Mode)").pack(anchor=W)
        self.line_x_slider = Scale(control_frame, from_=0, to=self.width, orient=HORIZONTAL, 
                                   command=self.update_line_x)
        self.line_x_slider.set(self.line_point[0])
        self.line_x_slider.pack(fill=X)
        
        Label(control_frame, text="Line Y (Linear Mode)").pack(anchor=W)
        self.line_y_slider = Scale(control_frame, from_=0, to=self.height, orient=HORIZONTAL, 
                                   command=self.update_line_y)
        self.line_y_slider.set(self.line_point[1])
        self.line_y_slider.pack(fill=X)
        
        Label(control_frame, text="Line Angle (Degrees)").pack(anchor=W)
        self.line_angle_slider = Scale(control_frame, from_=0, to=360, orient=HORIZONTAL, 
                                       command=self.update_line_angle)
        self.line_angle_slider.set(self.line_angle)
        self.line_angle_slider.pack(fill=X)
        
        Label(control_frame, text="Line Band (Thickness)").pack(anchor=W)
        self.line_band_slider = Scale(control_frame, from_=10, to=200, orient=HORIZONTAL, 
                                      command=self.update_line_band)
        self.line_band_slider.set(self.line_band)
        self.line_band_slider.pack(fill=X)
        
        
        Label(control_frame, text="Blur Strength").pack(anchor=W)
        self.blur_slider = Scale(control_frame, from_=0, to=50, orient=HORIZONTAL, 
                                command=self.update_blur)
        self.blur_slider.set(self.max_blur)
        self.blur_slider.pack(fill=X)
        
       
        Button(control_frame, text="Save Result", command=self.apply_blur).pack(pady=20)

    def drag_event(self, event):
        
        if self.blur_mode.get() == "radial":
            self.focal_point = (
                int(event.x / self.preview_scale),
                int(event.y / self.preview_scale)
            )
        else:
            self.line_point = (
                int(event.x / self.preview_scale),
                int(event.y / self.preview_scale)
            )
          
            self.line_x_slider.set(self.line_point[0])
            self.line_y_slider.set(self.line_point[1])
        self.update_display()

    def update_radius(self, val):
        self.radius = int(val)
        self.update_display()

    def update_blur(self, val):
        self.max_blur = int(val)
        self.update_display()

    def update_line_x(self, val):
        self.line_point = (int(val), self.line_point[1])
        self.update_display()

    def update_line_y(self, val):
        self.line_point = (self.line_point[0], int(val))
        self.update_display()

    def update_line_angle(self, val):
        self.line_angle = int(val)
        self.update_display()

    def update_line_band(self, val):
        self.line_band = int(val)
        self.update_display()

    def update_display(self):
        # Create a preview copy
        preview = self.preview_image.copy()
        draw = ImageDraw.Draw(preview)
        mode = self.blur_mode.get()
        if mode == "radial":
            
            preview_center = (
                int(self.focal_point[0] * self.preview_scale),
                int(self.focal_point[1] * self.preview_scale)
            )
            preview_radius = self.radius * self.preview_scale
            draw.ellipse([
                preview_center[0] - preview_radius,
                preview_center[1] - preview_radius,
                preview_center[0] + preview_radius,
                preview_center[1] + preview_radius
            ], outline="red", width=2)
        else:
            
            angle_rad = math.radians(self.line_angle)
            
            diag = math.hypot(self.width, self.height) * self.preview_scale
            dx = math.cos(angle_rad) * diag / 2
            dy = math.sin(angle_rad) * diag / 2
            x0 = self.line_point[0] * self.preview_scale - dx
            y0 = self.line_point[1] * self.preview_scale - dy
            x1 = self.line_point[0] * self.preview_scale + dx
            y1 = self.line_point[1] * self.preview_scale + dy
            draw.line([(x0, y0), (x1, y1)], fill="blue", width=2)
            
            offset = self.line_band * self.preview_scale / 2
            
            perp_dx = -math.sin(angle_rad) * offset
            perp_dy = math.cos(angle_rad) * offset
            draw.line([(x0 + perp_dx, y0 + perp_dy), (x1 + perp_dx, y1 + perp_dy)], fill="blue", width=1)
            draw.line([(x0 - perp_dx, y0 - perp_dy), (x1 - perp_dx, y1 - perp_dy)], fill="blue", width=1)
        
        
        self.tk_image = ImageTk.PhotoImage(preview)
        self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)
        self.canvas.image = self.tk_image

    def apply_blur(self):
        mode = self.blur_mode.get()
        mask = Image.new('L', (self.width, self.height), 0)
        draw = ImageDraw.Draw(mask)
        
        if mode == "radial":
            
            draw.ellipse([
                self.focal_point[0] - self.radius,
                self.focal_point[1] - self.radius,
                self.focal_point[0] + self.radius,
                self.focal_point[1] + self.radius
            ], fill=0)
            
            for y in range(self.height):
                for x in range(self.width):
                    distance = math.hypot(x - self.focal_point[0], y - self.focal_point[1])
                    if distance > self.radius:
                        normalized_distance = (distance - self.radius) / (math.hypot(self.width, self.height) - self.radius)
                        intensity = self.calculate_intensity(normalized_distance)
                        mask.putpixel((x, y), intensity)
        else:
            
            
            corners = [(0,0), (self.width,0), (0,self.height), (self.width,self.height)]
            angle_rad = math.radians(self.line_angle)
            
            def perp_distance(x, y):
                return abs((y - self.line_point[1]) * math.cos(angle_rad) - (x - self.line_point[0]) * math.sin(angle_rad))
            max_distance = max(perp_distance(x,y) for (x,y) in corners)
            half_band = self.line_band / 2.0
            for y in range(self.height):
                for x in range(self.width):
                    d = perp_distance(x, y)
                    if d < half_band:
                        intensity = 0
                    else:
                        normalized_distance = (d - half_band) / (max_distance - half_band)
                        intensity = self.calculate_intensity(normalized_distance, falloff="linear")
                    mask.putpixel((x, y), intensity)
        
        
        blurred_image = self.original_image.filter(ImageFilter.GaussianBlur(self.max_blur))
      
        final_image = Image.composite(blurred_image, self.original_image, mask)
        final_image.save("output_blur.jpg")
        print("Saved output_blur.jpg")

    def calculate_intensity(self, normalized_distance, falloff=None):
       
        if falloff is None:
            falloff = self.falloff_type if hasattr(self, 'falloff_type') else 'gaussian'
        if falloff == 'linear':
            return int(normalized_distance * 255)
        elif falloff == 'exponential':
            return int(255 * (1 - math.exp(-5 * normalized_distance)))
        elif falloff == 'gaussian':
            return int(255 * (1 - math.exp(- (normalized_distance ** 2) / 0.1)))
        return 0

if __name__ == "__main__":
    root = Tk()
    app = RadialBlurUI(root, "output_exposure.png")
    root.mainloop()
