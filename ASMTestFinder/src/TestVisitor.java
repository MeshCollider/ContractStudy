import org.objectweb.asm.AnnotationVisitor;
import org.objectweb.asm.Attribute;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.FieldVisitor;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;

public class TestVisitor extends ClassVisitor {

	private String name;
	private boolean isTestClass;
	
	public TestVisitor(int api) {
		super(api);
	}

	@Override
	public void visit(int version, int access, String name, String signature, String superName, String[] interfaces) {
		this.name = name;
		//System.out.println("Visiting class: " + name);
		
		String[] parts = this.name.split("/");
		String className = parts[parts.length-1];
		if (className.startsWith("Test")) {
			this.isTestClass = true;
			//System.out.println("This is a test class");
		}
		super.visit(version, access, name, signature, superName, interfaces);
	}

    @Override
    public AnnotationVisitor visitAnnotation(String desc, boolean visible) {
        //System.out.println("Annotation: " + desc);
        return super.visitAnnotation(desc, visible);
    }
    
    @Override
    public void visitAttribute(Attribute attr) {
        //System.out.println("Class Attribute: " + attr.type);
        super.visitAttribute(attr);
    }
    
    @Override
    public FieldVisitor visitField(int access, String name, String desc, String signature, Object value) {
        //System.out.println("Field: " + name + " " + desc + " value:" + value);
        return super.visitField(access, name, desc, signature, value);
    }
    
	@Override
	public MethodVisitor visitMethod(int access, String name, String desc, String signature, String[] exceptions) {
		/* if ((access & Opcodes.ACC_PUBLIC) != 0
				&& (access & Opcodes.ACC_STATIC) != 0
				&& "main".equals(name)
				&& "([Ljava/lang/String;)V".equals(desc)) {
			isTestClass = true;
		} */
		//System.out.println("Method: " + name + " " + desc);
		return super.visitMethod(access, name, desc, signature, exceptions);
	}
	
    
    @Override
    public void visitEnd() {
        //System.out.println("Method ends here");
        super.visitEnd();
    }

	public String getName() {
		return name;
	}

	public boolean isTestClass() {
		return isTestClass;
	}       
}